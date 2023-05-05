import streamlit as st
from streamlit_chat import message
import openai
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
openai.organization = os.getenv('OPENAI_ORGANIZATION_ID')

# Setting page title and header
st.set_page_config(page_title='SongChat', page_icon=':music:')
st.markdown('<h1 style="text-align: center;">SongChat - a demo of ChatGPT with local data</h1>', unsafe_allow_html=True)

# Initialise session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "You are conversationalist based on song lyrics."}
    ]
if 'model_name' not in st.session_state:
    st.session_state['model_name'] = []
if 'cost' not in st.session_state:
    st.session_state['cost'] = []
if 'total_tokens' not in st.session_state:
    st.session_state['total_tokens'] = []
if 'total_cost' not in st.session_state:
    st.session_state['total_cost'] = 0.0j

st.sidebar.title('Sidebar')
model_name = st.sidebar.radio('Choose a model:', ('GPT-3.5', 'GPT-4'))
counter_placeholder = st.sidebar.empty()
counter_placeholder.write(f'Total cost of this conversation: ${st.session_state["total_cost"]:.5f}')
clear_button = st.sidebar.button('Clear Conversation', key='clear')

# Map model names to OpenAI model IDs
if model_name == 'GPT-3.5':
    model = 'gpt-3.5-turbo'
else:
    model = 'gpt-4'

    # reset everything
if clear_button:
    st.session_state['generated'] = []
    st.session_state['past'] = []
    st.session_state['messages'] = [
        {"role": "system", "content": "You are conversationalist based on song lyrics."}
    ]
    st.session_state['number_tokens'] = []
    st.session_state['model_name'] = []
    st.session_state['cost'] = []
    st.session_state['total_cost'] = 0.0
    st.session_state['total_tokens'] = []
    counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")

# generate a response
def generate_response(prompt: str):
    st.session_state['messages'].append({'role': 'user', 'content': prompt})

    completion = openai.ChatCompletion.create(
        model=model,
        messages=st.session_state['messages']
    )
    response = completion.choices[0].message.content
    st.session_state['messages'].append({"role": "assistant", "content": response})

    # print(st.session_state['messages'])
    total_tokens = completion.usage.total_tokens
    prompt_tokens = completion.usage.prompt_tokens
    completion_tokens = completion.usage.completion_tokens
    return response, total_tokens, prompt_tokens, completion_tokens

