from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import urljoin

import aiohttp
import asyncio
import async_timeout

async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()

async def get_character_select(loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        character_select_url = 'http://rbnorway.org/t7-frame-data/'
        response = await fetch(session, character_select_url)
        soup = BeautifulSoup(response, "html.parser")

    for div in soup.select('div.entry.clearfix'):
        all_urls = div.findAll('a')
        for link in all_urls:
            if 't7-frames'not in link.get('href'):
                continue
            else:
                print('Found something.')
                webpage_downloader(link.get('href'))

def webpage_downloader(url):
    base_url = 'http://rbnorway.org/'
    character_url = url

    if base_url not in character_url:
        character_url = urljoin(base_url,character_url)

    file_name = character_url.replace('http://rbnorway.org/', '')
    file_name = file_name.replace('-t7-frames', '')
    file_name = file_name.replace('/', '')
    file_name = file_name.replace('-', '_')
    file_name = file_name.lower()
    file_name = file_name + '.html'

    print('Downloading: ' + file_name)
    # hahahahahahahaahahahahah
    urllib.request.urlretrieve(character_url, file_name)

loop = asyncio.get_event_loop()
loop.run_until_complete(get_character_select(loop))

# def webpagedl():
#     for div in soup.select('div.entry.clearfix'):
#         all_urls = div.findAll('a')
#         for link in all_urls:
#             if 't7-frames'not in link.get('href'):
#                 continue
#             else:
#                 webpage_downloader(link.get('href'))


