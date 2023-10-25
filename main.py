import streamlit as st
import openai
import base64
from PyPDF2 import PdfReader
import os

# Configure a sua chave de API da OpenAI aqui
openai.api_key = "YOUR_API_KEY_HERE"

def main():
    st.set_page_config(layout="wide")
    st.title('Aplicação de Perguntas e Respostas com OpenAI')

    st.sidebar.write('Faça o upload de um arquivo PDF e faça perguntas sobre o seu conteúdo.')
    uploaded_file = st.sidebar.file_uploader("Escolha um arquivo PDF", type=['pdf'])

    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if uploaded_file is not None:
            question = st.text_input('Faça uma pergunta sobre o conteúdo do arquivo:')
            if st.button('Perguntar'):
                if not question:
                    st.write('Por favor, insira uma pergunta.')
                else:
                    pdf_text = extract_text_from_pdf(uploaded_file)
                    answer = ask_question(pdf_text, question)
                    st.text_area('Resposta da OpenAI:', value=answer, height=200)

    with col2:
        if uploaded_file is not None:
            with open("temp_file.pdf", "wb") as file:
                file.write(uploaded_file.getbuffer())
            with open("temp_file.pdf", "rb") as file:
                pdf_base64 = base64.b64encode(file.read()).decode('utf-8')
                st.write(f'<iframe src="data:application/pdf;base64,{pdf_base64}" width="100%" height="600" style="border: none;"></iframe>',
                         unsafe_allow_html=True)
            os.remove("temp_file.pdf")

    with col3:
        st.write('Opções:')
        if st.button('Opção 1'):
            st.write('Você pressionou a Opção 1')
        if st.button('Opção 2'):
            st.write('Você pressionou a Opção 2')
        if st.button('Opção 3'):
            st.write('Você pressionou a Opção 3')

def extract_text_from_pdf(uploaded_file):
    pdf_reader = PdfReader(uploaded_file)
    pdf_text = ""
    for page in pdf_reader.pages:
        pdf_text += page.extract_text()
    return pdf_text

def ask_question(context, question):
    response = openai.Completion.create(
        engine="davinci",
        prompt=context + "\nQ: " + question + "\nA:",
        temperature=0.3,
        max_tokens=100
    )
    return response.choices[0].text.strip()

if __name__ == '__main__':
    main()
