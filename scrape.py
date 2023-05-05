import os    
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}

def fetch_link(link: Tag, artist: str):
    href = link.get('href')
    if href and href.startswith(f'https://www.songlyrics.com/{artist}/'):
       
        name = href.split('/')[-2]
        path = f'./{artist}/{name}.txt'
        print(name)

        if os.path.isfile(path):
            return

        reqs = requests.get(href, headers=headers)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        div = soup.find('p', {'id': 'songLyricsDiv'})
        if div:
            lyrics = div.get_text()
            with open(path, 'w') as f:
                f.write(lyrics)
                f.close()

def fetch(artist: str):
    if not os.path.exists(artist):
        os.makedirs(artist)

    url = f'https://www.songlyrics.com/{artist}-lyrics/'
    reqs = requests.get(url, headers=headers)
    soup = BeautifulSoup(reqs.text, 'html.parser')

    tracks = soup.find('table', {'class': 'tracklist'})
    if tracks:
        for link in tracks.find_all('a'):
            fetch_link(link, artist)

if __name__ == '__main__':
    [fetch(artist) for artist in ['wilco', 'radiohead', 'lada-gaga', 'hendrix-jimi']]
