
# importing necessary libraries
import pandas as pd
import streamlit as st
from pandasai import SmartDataframe
from pandasai.responses.response_parser import ResponseParser
from pandasai.llm import OpenAI
import matplotlib as plt

# define the customized streamlit output
class StreamlitOuput(ResponseParser):
    def __init__(self, context) -> None:
        super().__init__(context)
    def format_dataframe(self, result):  
        st.dataframe(result["value"])
        return
    def format_plot(self, result):
        st.image(result["value"])
        return
    def format_other(self, result):
        st.write(result["value"])
        return

# make the app wider
st.set_page_config(layout='wide')
# set the title
st.title ("  ChatBot : Jarvis ")
st.markdown('---') # to make line 

# file uploader using streamlit 
upload_xlsx_file = st.file_uploader("Uploader votre fichier XLSX pour l'analyser ou visualiser des données", type = ["xlsx"])
# if statement to make sure the data is uploaded
if upload_xlsx_file is not None:
    data = pd.read_excel(upload_xlsx_file)
    data.columns = data.columns.str.upper()   #convert the columns to uppercase 
    st.dataframe(data.head(5))
    st.write("Données uploadées avec succès")
st.markdown('---')
st.write ( "### Renseigner votre demande d'analyse ou de visualisation")
query = st.text_area(" Entrer votre prompt")


llm = OpenAI(api_token= st.secrets["chatgpt_token"])  ### API key starts with something sk-...
if st.button ("Envoyer"):
    if query:
        with st.spinner("Loading wait.."):
            st.write ( '### OUTPUT : ')
            st.markdown('---')
            # query_engine = SmartDataframe(data, config = {'llm':llm}) # without response parser -- data analysis only ( use the code below to display the visualization result as well
            query_engine = SmartDataframe(data, config = {'llm':llm, "response_parser": StreamlitOuput})
            answer = query_engine.chat(query)
            st.write(answer)
    else:
        st.warning("Entrer votre prompt")
