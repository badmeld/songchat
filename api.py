import openai
import pinecone
from dotenv import load_dotenv
import os

load_dotenv()

artists = os.getenv('ARTISTS').split(',')

openai.api_key = os.getenv('OPENAI_API_KEY')
openai.organization = os.getenv('OPENAI_ORGANIZATION_ID')
openai_model = os.getenv('OPENAI_EMBEDDING_MODEL')

pinecone_api_key = os.getenv('PINECONE_API_KEY')
pinecone_env = os.getenv('PINECONE_ENV') 
index_name = os.getenv('PINECONE_INDEX_NAME')

pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)
index = pinecone.Index(index_name)

def generate_embeddings(text: str) -> list:
    global openai_model
    response = openai.Embedding.create(model=openai_model, input=text)
    return response['data'][0]['embedding']

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