import random
import ast
from PyPDF2 import PdfReader

import streamlit as st


def string_to_list(s):

    try:
        return ast.literal_eval(s)
    
    except Exception as e:
        st.error(f"Error: The provided input is not correctly formatted. {e}")
        st.stop()


def get_randomized_options(options):
    correct_answer = options[0]
    random.shuffle(options)
    return options, correct_answer


def extract_pdf_text(docs) -> str:
    txt = ""
    for doc in docs:
        reader = PdfReader(doc)
        for page in reader.pages:
            txt += page.extract_text()
    return txt
