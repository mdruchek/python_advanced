import argparse
import asyncio
import re
from pathlib import Path

import aiohttp
import aiofiles
from bs4 import BeautifulSoup


OUT_PATH = Path(__file__).parent
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()

parser = argparse.ArgumentParser()
parser.add_argument('--url', help='URL')
parser.add_argument('--enclosure', help='Number of attachments', default=3)
args = parser.parse_args()
url = args.url
enclosure = int(args.enclosure)


async def write_to_file(link: str):
    file_path = "{}/{}".format(OUT_PATH, 'links.txt')
    async with aiofiles.open(file_path, mode='a+') as f:
        await f.seek(0)
        cont = await f.read()
        if cont != '\n':
            link_found = False
            async for line in f:
                if link == line:
                    link_found = True
                    break
        if not link_found:
            await f.write(link)


async def parse_url_current(session, url, enclosure, enclosure_current=0):
    try:
        async with session.get(url, timeout=5) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            links = []
            for link in soup.find_all('a'):
                link: str = link.get('href')
                if link is not None and link.startswith('http') and not link.startswith(url):
                    try:
                        link = re.match(r'https?:\/\/\S+?(?:(?:\/)|(?:.ru)|(?:.com)|(?:.рф)|(?:.org))', link).group(0)
                    except AttributeError:
                        continue
                    if link not in links:
                        # print(link)
                        await write_to_file(link + '\n')
                        links.append(link)
        for link in links:
            if enclosure_current == enclosure:
                return
            try:
                await parse_url_current(session, link, enclosure, enclosure_current + 1)
            except aiohttp.client_exceptions.ClientConnectorError:
                continue
    except asyncio.exceptions.TimeoutError:
        return


async def parse_urls_all(url: str, enclosure: int):
    async with aiohttp.ClientSession() as session:
        await parse_url_current(session, url, enclosure)


def main():
    asyncio.run(parse_urls_all(url, enclosure))


if __name__ == '__main__':
    main()
