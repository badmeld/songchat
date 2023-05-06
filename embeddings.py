import os
from api import generate_embeddings, upsert_embeddings, artists
from tqdm.auto import tqdm

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
        upsert_embeddings(vectors=records, namespace='lyrics')

if __name__ == '__main__':
    for artist in artists:
        lyrics = fetch_lyrics(artist)
        store_embeddings(artist, lyrics)
