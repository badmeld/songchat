import streamlit as st
from streamlit_chat import message
from api import generate_embeddings, query_db
import os

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

st.sidebar.title('Sidebar')
model_name = st.sidebar.radio('Choose a model:', ('GPT-3.5', 'GPT-4'))
counter_placeholder = st.sidebar.empty()
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

# generate a response
def generate_response(prompt: str):
    st.session_state['messages'].append({'role': 'user', 'content': prompt})

    #completion = openai.ChatCompletion.create(
    #    model=model,
    #    messages=st.session_state['messages']
    #)
    #response = completion.choices[0].message.content
    #st.session_state['messages'].append({"role": "assistant", "content": response})

    # print(st.session_state['messages'])
    #total_tokens = completion.usage.total_tokens
    #prompt_tokens = completion.usage.prompt_tokens
    #completion_tokens = completion.usage.completion_tokens
    #return response, total_tokens, prompt_tokens, completion_tokens

def search(prompt: str):
    embedding = generate_embeddings(prompt)
    results = query_db(embedding, ['wilco'])
    for match in results['matches']:
        print(match['metadata']['text'])

# container for chat history
response_container = st.container()
# container for text box
container = st.container()

with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("You:", key='input', height=100)
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        search(user_input)
        #output, total_tokens, prompt_tokens, completion_tokens = generate_response(user_input)
        #st.session_state['past'].append(user_input)
        #st.session_state['generated'].append(output)
        #st.session_state['model_name'].append(model_name)
        #st.session_state['total_tokens'].append(total_tokens)

        # from https://openai.com/pricing#language-models
        #if model_name == "GPT-3.5":
        #    cost = total_tokens * 0.002 / 1000
        #else:
        #    cost = (prompt_tokens * 0.03 + completion_tokens * 0.06) / 1000

        #st.session_state['cost'].append(cost)
        #st.session_state['total_cost'] += cost

#if st.session_state['generated']:
#    with response_container:
#        for i in range(len(st.session_state['generated'])):
#            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
#            message(st.session_state["generated"][i], key=str(i))
#            st.write(
#                f"Model used: {st.session_state['model_name'][i]}; Number of tokens: {st.session_state['total_tokens'][i]}; Cost: ${st.session_state['cost'][i]:.5f}")
#            counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")




