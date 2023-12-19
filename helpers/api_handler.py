import google.generativeai as palm


def authenticate_api_key(token) -> bool:
    request = get_api_response("", "", token)

    if request == False:
        return False

    return True


def get_api_response(context, question, token):
    try:
        out_of_context_responses = [
            "I'm sorry, the answer to that question isn't in the provided PDF.",
            "It seems the information you're looking for might not be in the PDF.",
            "The PDF doesn't seem to cover that particular question.",
            "That's outside the scope of the information in the PDF.",
            "Unfortunately, the PDF doesn't contain details on that question.",
            "It looks like the PDF doesn't have the answer you're seeking.",
            "I can't find the answer to your question within the PDF.",
            "The PDF may not include information relevant to your question.",
            "This question might not have been addressed in the PDF.",
            "I'm afraid I couldn't locate an answer to your question in the PDF. Please try again with any different question.",
        ]
        import random

        response = random.choice(out_of_context_responses)

        prompt = f"""
        You are a helpful, respectful, and honest assistant dedicated to providing informative and accurate response based on provided context((delimited by <ctx></ctx>)) only. You don't derive
        answer outside context, while answering your answer should be precise, accurate, clear and should not be verbose and only contain answer. In context you will have texts which is unrelated to question,
        please ignore that context only answer from the related context only. Do not answer anything out of the context provided. If any such case arises then simply return {response}.
        If the question is unclear, incoherent, or lacks factual basis, please clarify the issue rather than generating inaccurate information. This is to be strictly followed while answering.
        if the question is about viewing the past questions and answers then reply by saying "Please scroll up to find the previous questions and answers".

        If formatting, such as bullet points, numbered lists, tables, bold texts, underlining texts, italics text or code blocks, is necessary for a comprehensive response, please apply the appropriate formatting.

        <ctx>
        CONTEXT:
        {context}
        </ctx>

        QUESTION:
        {question}

        ANSWER
        """

        palm.configure(api_key=token)

        models = [
            m
            for m in palm.list_models()
            if "generateText" in m.supported_generation_methods
        ]

        model = models[0].name

        completion = palm.generate_text(
            model=model,
            prompt=prompt,
            temperature=0.3,
            # The maximum length of the response
            # max_output_tokens=800,
        )
        return completion.result

    except:
        return False


def get_quiz_data(data, token,n):

    try:

        template = f"""
        You are a helpful assistant programmed to generate questions based on any text provided. For every chunk of text you receive, you're tasked with designing {n} distinct questions. Each of these questions will be accompanied by 3 possible answers: one correct answer and two incorrect ones. 

        For clarity and ease of processing, structure your response in a way that emulates a Python list of lists.

        Use the following data for generating the questions:

        "{data}" 

        Your output should be shaped as follows:

        1. An outer list that contains {n} inner lists.
        2. Each inner list represents a set of question and answers, and contains exactly 4 strings in this order:
        - The generated question.
        - The correct answer.
        - The first incorrect answer.
        - The second incorrect answer.

        Your output should mirror this structure:
        [
            ["Generated Question 1", "Correct Answer 1", "Incorrect Answer 1.1", "Incorrect Answer 1.2"],
            ["Generated Question 2", "Correct Answer 2", "Incorrect Answer 2.1", "Incorrect Answer 2.2"],
            ...
        ]

        It is crucial that you adhere to this format as it's optimized for further Python processing.

        """

        palm.configure(api_key=token)


        # Set up the model
        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }

        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
        ]

        model = palm.GenerativeModel(
            model_name="gemini-pro",
            generation_config=generation_config,
            safety_settings=safety_settings,
        )

        response = model.generate_content(template)

        return response.text
    
    except:

        return False
