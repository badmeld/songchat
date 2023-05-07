import streamlit as st
from streamlit_chat import message
from api import generate_embeddings, query_db, generate_prompt, generate_completion
import os

# Setting page title and header
st.set_page_config(page_title='SongChat', page_icon=':music:')
st.markdown('<h1 style="text-align: center;">SongChat - a demo of ChatGPT with local data</h1>', unsafe_allow_html=True)

st.sidebar.title('Sidebar')
clear_button = st.sidebar.button('Clear Conversation', key='clear')

    # reset everything
if clear_button:
    pass

# generate a response
def generate_response(prompt: str):
    
    embedding = generate_embeddings(prompt)
    results = query_db(embedding, ['wilco'])
    context = []

    for match in results['matches']:
        context.append(match['metadata']['text'])

    prompt = generate_prompt(prompt, context)
    
    return generate_completion(prompt)

# container for chat history
response_container = st.container()
# container for text box
container = st.container()

with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("You:", key='input', height=100)
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        output = generate_response(user_input)
        message(output)




