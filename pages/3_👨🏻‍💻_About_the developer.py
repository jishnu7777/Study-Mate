from pathlib import Path

import streamlit as st
from PIL import Image


# --- PATH SETTINGS ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "styles" / "main.css"
resume_file = current_dir / "assets" / "CV.pdf"
profile_pic = current_dir / "assets" / "profile-pic.png"


# --- GENERAL SETTINGS ---
PAGE_TITLE = "Study Mate"
PAGE_ICON = ":books:"
NAME = "Jishnu Saha"
DESCRIPTION = """
An engineering undergrad with a passion for coding and technology, adept at solving intricate problems while envisioning innovative solutions across diverse domains.
"""
EMAIL = "jishnusahawork@email.com"
SOCIAL_MEDIA = {
    "YouTube": "https://youtube.com/c/Jishnu69",
    "LinkedIn": "https://www.linkedin.com/in/jishnu-saha7777",
    "GitHub": "https://github.com/jishnu7777",
    "Instagram": "https://www.instagram.com/jishnu_2069/",
}
PROJECTS = {
    "📚🤖 **Study Mate** - a web app that simplifies learning by allowing students to query PDF content and generates personalized multiple-choice questions, enhancing study efficiency": "https://github.com/jishnu7777/Study-Mate.git"}


st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)


# --- LOAD CSS, PDF & PROFIL PIC ---
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)
#with open(resume_file, "rb") as pdf_file:
   # PDFbyte = pdf_file.read()
profile_pic = Image.open(profile_pic)


# --- HERO SECTION ---
col1, col2 = st.columns(2, gap="small")
with col1:
    st.image(profile_pic, width=230)

with col2:
    st.title(NAME)
    st.write(DESCRIPTION)
    #st.download_button(
        #label=" 📄 Download Resume",
        #data=PDFbyte,
        #file_name=resume_file.name,
        #mime="application/octet-stream",)
    st.write("📫", EMAIL)


# --- SOCIAL LINKS ---
st.write("\n")
cols = st.columns(len(SOCIAL_MEDIA))
for index, (platform, link) in enumerate(SOCIAL_MEDIA.items()):
    cols[index].write(f"[{platform}]({link})")


# --- EXPERIENCE & QUALIFICATIONS ---
st.write("\n")
st.subheader("Experience & Qualifications")
st.write(
    """
- ✔️ Pursuing B.Tech in Electronics and Communications Technology (ECE) from IEM Kolkata
- ✔️ Strong hands on experience and knowledge in Python
- ✔️ Excellent team-player and displaying strong sense of initiative on tasks
"""
)


# --- SKILLS ---
st.write("\n")
st.subheader("Technical Skills")
st.write(
    """
- 👩‍💻 Programming Languages: Python, C++, HTML, CSS
- :hammer_and_wrench: Frameworks: Streamlit
- 🗄️ Databases: MySQL
"""
)



# --- Projects & Accomplishments ---
st.write("\n")
st.subheader("Projects")
st.write("---")
for project, link in PROJECTS.items():
    st.write(f"[{project}]({link})")
