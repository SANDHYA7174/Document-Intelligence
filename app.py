import streamlit as st
from PIL import Image
import fitz
import pytesseract
from gtts import gTTS
from llm import ask_question,summarize

st.set_page_config(page_title="Document Analyzer")
st.title("📄 Document & Image Analyzer (Gemini)")

uploaded=st.file_uploader("Upload PDF/Image",type=["pdf","png","jpg","jpeg"])

text=""
if uploaded:
    if uploaded.name.lower().endswith(".pdf"):
        pdf=fitz.open(stream=uploaded.read(),filetype="pdf")
        for page in pdf:
            text+=page.get_text()
    else:
        img=Image.open(uploaded)
        st.image(img,caption="Uploaded Image")
        text=pytesseract.image_to_string(img)

    st.subheader("Extracted Text")
    st.text_area("",text,height=250)

    q=st.text_input("Ask a question")
    if st.button("Answer") and q:
        st.success(ask_question(text,q))

    if st.button("Generate Summary"):
        s=summarize(text)
        st.subheader("Summary")
        st.write(s)
        tts=gTTS(s)
        tts.save("summary.mp3")
        with open("summary.mp3","rb") as f:
            st.audio(f.read(),format="audio/mp3")
            st.download_button("Download Audio",f,file_name="summary.mp3")
        