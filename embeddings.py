import openai
import os
import pinecone
from tqdm.auto import tqdm
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
openai_model = os.getenv('OPENAI_EMBEDDING_MODEL')
pinecone_api_key = os.getenv('PINECONE_API_KEY')
pinecone_env = os.getenv('PINECONE_ENV')
index_name = os.getenv('PINECONE_INDEX_NAME')

pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)
index = pinecone.Index(index_name)

lyrics = []

def fetch_lyrics(artist: str) -> list:
    lyrics = [] 
    for file_name in os.listdir(artist):
        if file_name.endswith('.txt'):
            file_path = os.path.join(artist, file_name)
            with open(file_path, 'r') as file:
                text = file.read()
                name = file_name.rstrip('-lyrics.txt')
                lyrics.append((artist, name, text))
    return lyrics

def generate_embeddings(text: str) -> list:
    response = openai.Embedding.create(model=openai_model, input=text)
    return response['data'][0]['embedding']

def store_embeddings(artist: str, lyrics: list):

    print(f'storing embeddings for {artist}') 

    batch_size = 16

    for i in tqdm(range(0, len(lyrics), batch_size)):

        # find end of batch
        i_end = min(i+batch_size, len(lyrics))
        
        # create IDs batch
        ids = [f'{artist}-{x}' for x in range(i, i_end)]
        
        # create metadata batch
        metadatas = [{'text': lyric[2], 'artist': lyric[0], 'song': lyric[1]} for lyric in lyrics[i:i_end]]

        xc = []
        for i in range(i, i_end):
            xc.append(generate_embeddings(lyrics[i][2]))
        
        # create records list for upsert
        records = zip(ids, xc, metadatas)
        
        # upsert to Pinecone
        index.upsert(vectors=records, namespace='lyrics')

if __name__ == '__main__':
    #for artist in ['drake', 'wilco', 'radiohead', 'lady-gaga', 'hendrix-jimi']:
    for artist in ['lady-gaga', 'hendrix-jimi']:
        lyrics = fetch_lyrics(artist)
        store_embeddings(artist, lyrics)
