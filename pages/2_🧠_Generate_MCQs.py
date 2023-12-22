import streamlit as st
from helpers.quiz_utils import extract_pdf_text
from helpers.api_handler import get_quiz_data, authenticate_api_key
from helpers.quiz_utils import string_to_list, get_randomized_options
from helpers.toast_messages import get_random_toast


st.set_page_config(page_title="Study Mate", page_icon=":books:", layout="centered")

# Check if user is new or returning using session state.
# If user is new, show the toast message.
if "first_time" not in st.session_state:
    message, icon = get_random_toast()
    st.toast(message, icon=icon)
    st.session_state.first_time = False

if "GOOGLE_API_TOKEN" not in st.session_state:
    st.session_state.GOOGLE_API_TOKEN = None

if "pdf_docs" not in st.session_state:
    st.session_state.pdf_docs = None

if "pdf_data" not in st.session_state:
    st.session_state.pdf_data = None

if "submission_verifier" not in st.session_state:
    st.session_state.submission_verifier = False

if "key_verifier" not in st.session_state:
    st.session_state.key_verifier = True


st.title(":red[Generate MCQs] 🧠", anchor=False)
st.write(
    """
Ever read a pdf document and wondered how well you understood its content? Here's a fun twist: Instead of just reading PDFs, come to **MCQ Wizard** and test your comprehension!

**How does it work?** 🤔
1. Upload the PDF document based on which you want the bot to generate questions.
2. Enter your [Google API Key](https://makersuite.google.com/app/apikey).

⚠️ **IMPORTANT INSTRUCTIONS**⚠️: 
1. The contents of the PDF must be in English language for the bot to work.
2. Please wait while the page displays 'RUNNING' in the top right corner.
3. The bot might take some time to process, depending on the number of questions you have chosen to answer.
4. Refresh the page every time you want to upload a new PDF or when you want to change the number of questions.

Once you've input the details, voilà! Dive deep into questions crafted just for you, ensuring you've truly grasped the content of the PDF. Let's put your knowledge to the test! 
"""
)

with st.expander("🎥 Video Tutorial"):
    with st.spinner("Loading video.."):
        st.video("https://youtu.be/8BExf2rU5Dg", format="video/mp4", start_time=0)

temp3 = st.empty()

with temp3.form("user_input"):
    pdf_docs = st.file_uploader(
        "Upload your documents here and click on the submit button",
        accept_multiple_files=True,
        type=["pdf"],
    )

    st.session_state.pdf_docs = pdf_docs

    if st.session_state.pdf_docs:
        st.session_state.submission_verifier = True

    temp2 = st.empty()

    GOOGLE_API_TOKEN = temp2.text_input(
        "Enter your Google Makersuite API Token:",
        placeholder="AIXXXX",
        type="password",
        value=st.session_state.GOOGLE_API_TOKEN,
    )
    st.session_state.GOOGLE_API_TOKEN = GOOGLE_API_TOKEN

    if st.session_state.GOOGLE_API_TOKEN:
        if not authenticate_api_key(st.session_state.GOOGLE_API_TOKEN):
            st.session_state.key_verifier = False

        if authenticate_api_key(st.session_state.GOOGLE_API_TOKEN):
            st.session_state.key_verifier = True

    temp1 = st.empty()

    n = temp1.slider(
        "Select the number of questions you want the bot to generate..",
        min_value=5,
        max_value=20,
    )

    submitted = st.form_submit_button("Craft my quiz!")

if submitted or ("quiz_data_list" in st.session_state):
    if not st.session_state.pdf_docs and not st.session_state.submission_verifier:
        st.error("Please upload a valid pdf document.")
        st.stop()
    elif not st.session_state.GOOGLE_API_TOKEN:
        st.error(
            "Please fill out the Google API Key to proceed. If you don't have one, you can obtain it [here](https://makersuite.google.com/app/apikey)."
        )
        st.stop()
    elif not st.session_state.key_verifier:
        st.error(
            "Invalid Google Makersuite API Token⚠️. Please refresh and retry or else if you don't have one, you can obtain it [here](https://makersuite.google.com/app/apikey)."
        )
        st.stop()

    else:
        temp1.empty()
        temp2.empty()
        temp3.empty()

    with st.spinner("Crafting your quiz...🤓"):
        if submitted:
            pdf_data = str(extract_pdf_text(st.session_state.pdf_docs))

            # print("PDF DATA : ", pdf_data)

            st.session_state.pdf_data = pdf_data
            quiz_data_str = get_quiz_data(
                st.session_state.pdf_data, st.session_state.GOOGLE_API_TOKEN, n
            )

            # print("LLM output :", quiz_data_str)

            st.session_state.quiz_data_list = string_to_list(quiz_data_str)

            # print(st.session_state.quiz_data_list)

            if "user_answers" not in st.session_state:
                st.session_state.user_answers = [
                    None for _ in st.session_state.quiz_data_list
                ]
            if "correct_answers" not in st.session_state:
                st.session_state.correct_answers = []
            if "randomized_options" not in st.session_state:
                st.session_state.randomized_options = []

            for q in st.session_state.quiz_data_list:
                options, correct_answer = get_randomized_options(q[1:])
                st.session_state.randomized_options.append(options)
                st.session_state.correct_answers.append(correct_answer)

        try:
            with st.form(key="quiz_form"):
                st.subheader("🧠 Quiz Time: Test Your Knowledge!", anchor=False)
                for i, q in enumerate(st.session_state.quiz_data_list):
                    options = st.session_state.randomized_options[i]
                    default_index = (
                        st.session_state.user_answers[i]
                        if st.session_state.user_answers[i] is not None
                        else 0
                    )
                    response = st.radio(q[0], options, index=default_index)
                    user_choice_index = options.index(response)
                    st.session_state.user_answers[
                        i
                    ] = user_choice_index  # Update the stored answer right after fetching it

                results_submitted = st.form_submit_button(label="Unveil My Score!")

                if results_submitted:
                    score = sum(
                        [
                            ua == st.session_state.randomized_options[i].index(ca)
                            for i, (ua, ca) in enumerate(
                                zip(
                                    st.session_state.user_answers,
                                    st.session_state.correct_answers,
                                )
                            )
                        ]
                    )
                    st.success(
                        f"Your score: {score}/{len(st.session_state.quiz_data_list)}"
                    )

                    if score == len(
                        st.session_state.quiz_data_list
                    ):  # Check if all answers are correct
                        st.balloons()
                    else:
                        incorrect_count = len(st.session_state.quiz_data_list) - score
                        if incorrect_count == 1:
                            st.warning(
                                f"Almost perfect! You got 1 question wrong. Let's review it:"
                            )
                        else:
                            st.warning(
                                f"Almost there! You got {incorrect_count} questions wrong. Let's review them:"
                            )

                    for i, (ua, ca, q, ro) in enumerate(
                        zip(
                            st.session_state.user_answers,
                            st.session_state.correct_answers,
                            st.session_state.quiz_data_list,
                            st.session_state.randomized_options,
                        )
                    ):
                        with st.expander(f"Question {i + 1}", expanded=False):
                            if ro[ua] != ca:
                                st.info(f"Question: {q[0]}")
                                st.error(f"Your answer: {ro[ua]}")
                                st.success(f"Correct answer: {ca}")

        except:
            st.error("Something went wrong. Please refresh the page and try again.")
            st.stop()
