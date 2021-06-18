import time
import asyncio

import requests
import aiohttp


# <------------ Последовательный код ------------>
def get_response(url):
    response = requests.get(url, allow_redirects=True)
    return response


def write_file(response):
    *_, file_name = response.url.split('/')
    with open(file_name, mode='wb') as file:
        file.write(response.content)


def download_file(url):
    time_start = time.time()

    for _ in range(10):
        write_file(get_response(url))

    time_end = time.time() - time_start
    print(time_end)

# ~4 sec runtime
# if __name__ == '__main__':
#     url_ = 'https://loremflickr.com/320/240'
#     download_file(url_)


# <------------ async решение (с одной not async функцией) ------------>
def write_image(data):
    filename = f'{int(time.time() * 1000)}.jpeg'
    with open(filename, mode='wb') as file:
        file.write(data)


async def fetch_content(url, session):
    async with session.get(url, allow_redirects=True) as response:
        data = await response.read()
        write_image(data)


async def async_download_file():
    url = 'https://loremflickr.com/320/240'
    tasks = []

    async with aiohttp.ClientSession() as session:
        for _ in range(10):
            task = asyncio.create_task(fetch_content(url, session))
            tasks.append(task)

        await asyncio.gather(*tasks)

# ~1 sec runtime
if __name__ == '__main__':
    time_start = time.time()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_download_file())

    time_end = time.time() - time_start
    print(time_end)
