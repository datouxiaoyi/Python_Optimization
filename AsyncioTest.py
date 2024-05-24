import asyncio
import threading
import aiohttp
import time
import requests

async def fetch_page(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
        
async def compute_length(url):
    page = await fetch_page(url)
    return len(page)

async def async_main():
    urls = ["http://www.example.com"]*10
    tasks = [compute_length(url) for url in urls]
    results = await asyncio.gather(*tasks)
    print("内容长度为:", results)

def thread_fetch_page(url):
    response = requests.get(url)
    return response.text
def thread_compute_length(url):
    page = thread_fetch_page(url)
    return len(page)
def thread_main():
    urls = ["http://www.example.com"]*10    
    threads = []
    results = []
    start_time = time.time()
    for url in urls:
        thread = threading.Thread(target=lambda u: results.append(thread_compute_length(u)), args=(url,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    end_time = time.time()
    print("内容长度为:", results)
    print(f"使用多线程时间为: {end_time - start_time} 秒")    

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(async_main())
    end_time = time.time()
    print(f"使用协程时间为: {end_time - start_time} 秒")
    thread_main()



