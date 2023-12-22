import streamlit as st
from helpers.htmlTemplates import css, bot_template, user_template
import time
import helpers.api_handler as api_handler
from helpers.quiz_utils import extract_pdf_text





def display_chat():
    for i, message in enumerate(st.session_state.conversation):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message), unsafe_allow_html=True)

        else:
            st.write(bot_template.replace("{{MSG}}", message), unsafe_allow_html=True)


def main():
    st.set_page_config(page_title="Study Mate",page_icon=":books:", layout="centered")

    st.write(css, unsafe_allow_html=True)

    if "raw_txt" not in st.session_state:
        st.session_state.raw_txt = None

    if "submission_verifier" not in st.session_state:
        st.session_state.submission_verifier = False

    if "token_verifier" not in st.session_state:
        st.session_state.token_verifier = False

    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    if "pdf_docs" not in st.session_state:
        st.session_state.pdf_docs = None

    if "GOOGLE_API_TOKEN" not in st.session_state:
        st.session_state.GOOGLE_API_TOKEN = None

    st.title("Ask questions 💬")

    user_question = st.text_input("Ask any questions about your uploaded documents:")

    with st.sidebar:
        with st.form("user_input"):
            GOOGLE_API_TOKEN = st.text_input(
                "Enter your Google Makersuite API Token:",
                placeholder="AIXXXX",
                type="password",
                value=st.session_state.GOOGLE_API_TOKEN,
            )

            st.session_state.GOOGLE_API_TOKEN = GOOGLE_API_TOKEN

            submitted = st.form_submit_button("Submit")

            if submitted:
                if not st.session_state.GOOGLE_API_TOKEN:
                    st.info(
                        "Please fill out the Google Makersuite API Token to proceed. If you don't have one, you can obtain it [here](https://makersuite.google.com/app/apikey)."
                    )
                    st.stop()

                else:
                    with st.spinner("Verifying..."):
                        if api_handler.authenticate_api_key(st.session_state.GOOGLE_API_TOKEN):
                            alert = st.success("Successfully verified✔️")
                            time.sleep(1)
                            alert.empty()
                            st.session_state.token_verifier = True

                        else:
                            st.error(
                                "Invalid Google Makersuite API Token⚠️. Please refresh and retry or else if you don't have one, you can obtain it [here](https://makersuite.google.com/app/apikey)."
                            )

        if st.session_state.token_verifier:
            st.subheader("Your Documents")

            pdf_docs = st.file_uploader(
                "Upload your documents here and click on the submit button",
                accept_multiple_files=True,
                type=["pdf"],
            )

            st.session_state.pdf_docs = pdf_docs

            if st.button("Submit") and st.session_state.pdf_docs:
                st.session_state.submission_verifier = True

                with st.spinner("Loading..."):
                    raw_txt = extract_pdf_text(pdf_docs)

                    st.session_state.raw_txt = raw_txt

                    time.sleep(1)

                    st.success("Your document has been successfully uploaded✔️.")

                    time.sleep(1)

                    st.info("You may now ask the bot questions about your document....")

    if user_question == "\cc" and st.session_state.submission_verifier:
        try:
            st.session_state.conversation.clear()

            st.success("Chat history successfully deleted")

        except:
            st.error(
                "Oops! Sorry the bot ran into a problem. Please refresh the page and try again"
            )
            st.info(
                "Or please try again using a smaller pdf (small in terms of no. of pages)"
            )
            st.stop()

    if user_question and st.session_state.submission_verifier:
        if user_question != "\cc":
            try:
                output = api_handler.get_api_response(
                    st.session_state.raw_txt,
                    user_question,
                    st.session_state.GOOGLE_API_TOKEN,
                )

                st.session_state.conversation.append(user_question)
                st.session_state.conversation.append(output)

                display_chat()

            except:
                st.error(
                    "Oops! Sorry the bot ran into a problem. Please refresh the page and try again"
                )
                st.info(
                    "Or please try again using a smaller pdf (small in terms of no. of pages)"
                )
                st.stop()


if __name__ == "__main__":
    main()
