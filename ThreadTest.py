import threading
import time
import requests


def fetch_url(url: str)->None:
    '''根据地址发起请求，获取响应
    - url: 请求地址'''
    response = requests.get(url)
    print(f"{url}: {response.status_code}")

def fetch_urls_sequential(urls:list)->None:
    start_time = time.time()
    for url in urls:
        fetch_url(url)
    end_time = time.time()
    print(f"使用单线程时间为: {end_time - start_time} 秒\n")


def fetch_urls_concurrent(urls:list)->None:
    start_time = time.time()
    threads = []
    for url in urls:
        thread = threading.Thread(target=fetch_url, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    end_time = time.time()
    print(f"使用多线程时间为: {end_time - start_time} 秒")

if __name__ == "__main__":
    urls = ["http://www.example.com"]*10
    fetch_urls_sequential(urls)
    fetch_urls_concurrent(urls)
