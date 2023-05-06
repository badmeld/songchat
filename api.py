import openai
import pinecone
from dotenv import load_dotenv
import tiktoken
import os

load_dotenv()

artists = os.getenv('ARTISTS').split(',')
tke = tiktoken.get_encoding('cl100k_base')

openai.api_key = os.getenv('OPENAI_API_KEY')
openai.organization = os.getenv('OPENAI_ORGANIZATION_ID')
openai_embedding_model = os.getenv('OPENAI_EMBEDDING_MODEL')
openai_chat_model = os.getenv('OPENAI_CHAT_MODEL')
token_limit = int(os.getenv('OPENAI_TOKEN_LIMIT'))

pinecone_api_key = os.getenv('PINECONE_API_KEY')
pinecone_env = os.getenv('PINECONE_ENV') 
index_name = os.getenv('PINECONE_INDEX_NAME')

pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)
index = pinecone.Index(index_name)

def generate_prompt(text: str, context: list) -> str:
    prompt = [] 
    prompt.append('Context:')

    global tke
    global token_limit
    token_count = len(tke.encode(prompt[0])) + len(tke.encode(text))

    for ctxt in context:
        token_count += len(tke.encode(ctxt))
        if token_count >= token_limit:
            break
        else:
            prompt.append(ctxt)
    
    prompt.append('Question:')
    prompt.append(text)

    pstr = '\n'.join(prompt)
    print(pstr)
    print(f'token count: {token_count}')

    return pstr
    
def generate_embeddings(text: str) -> list:
    global openai_embedding_model
    response = openai.Embedding.create(model=openai_embedding_model, input=text)
    return response['data'][0]['embedding']

def generate_completion(prompt: str) -> str:
    global openai_chat_model
    messages = [
        { 
            'role': 'system', 
            'content': '''You are a philosopher and spiritual guide who provides amusing advice based on song 
                        lyrics included in the context. Do not quote the lyrics directly, sythesize advice based
                        on the meaning of the lyrics so it feels like the user is having a conversation with
                        the person who wrote the lyrics.'''
        },
        {
            'role': 'user',
            'content': prompt
        }
    ]
    completion = openai.ChatCompletion.create(
        model=openai_chat_model,
        messages=messages
    )
    return completion.choices[0].message.content

def upsert_embeddings(vectors: list, namespace: str):
    global index
    index.upsert(vectors=vectors, namespace=namespace)

def query_db(query: list, artists: list):
    global index
    return index.query(
        namespace='lyrics',
        top_k=10,
        include_values=True,
        include_metadata=True,
        vector=query,
        filter={
            'artist': {'$in': artists}
        }
    )