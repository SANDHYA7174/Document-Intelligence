import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0
)


def ask_question(document, question):
    prompt = PromptTemplate.from_template(
        """Answer ONLY using the document.

Document:
{document}

Question:
{question}
"""
    )

    chain = prompt | llm

    return chain.invoke({
        "document": document,
        "question": question
    }).content


def summarize(document):
    prompt = PromptTemplate.from_template(
        """Summarize this document in 5 concise bullet points.

{document}
"""
    )

    chain = prompt | llm

    return chain.invoke({
        "document": document
    }).content