# 一、多线程

在CPU不密集、IO密集的任务下，多线程可以一定程度的提升运行效率。

```
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
```

> http://www.example.com: 200
>
> http://www.example.com: 200
>
> http://www.example.com: 200
>
> http://www.example.com: 200
>
> http://www.example.com: 200
>
> http://www.example.com: 200
>
> http://www.example.com: 200
>
> http://www.example.com: 200
>
> http://www.example.com: 200
>
> http://www.example.com: 200
>
> 使用单线程时间为: 10.178432703018188 秒
>
>   
>
>
> http://www.example.com: 200
>
> http://www.example.com: 200
>
> http://www.example.com: 200
>
> http://www.example.com: 200
>
> http://www.example.com: 200
>
> http://www.example.com: 200
>
> http://www.example.com: 200
>
> http://www.example.com: 200
>
> http://www.example.com: 200
>
> http://www.example.com: 200
>
> 使用多线程时间为: 0.5794060230255127 秒

可以看到在IO密集型任务时，排除极端情况，使用多线程可以很大的提升程序的性能。例如在这个例子中，响应时间就相差了8倍多。

虽然在Python中有GIL保护机制，但是依然需要注意线程安全。例如（共享数据、共享设备、非原子性操作等）。可以使用锁机制、信号机制、队列、管道等等。

# 二、协程

协程也叫轻量级线程，协程是一种在单一线程内实现并发编程的技术。它们允许函数在执行过程中暂停，并在稍后恢复，从而使得多个任务能够交替执行，而不需要多个操作系统线程的开销。协程通过让出控制权来暂停执行，等待其他协程运行，然后在适当的时候恢复执行。

| 区别    | 线程                          | 协程                          |
| ----- | --------------------------- | --------------------------- |
| 上下文切换 | 线程上下文切换由操作系统决定，消耗更大         | 协程的上下文切换由用户自己决定，消耗更小        |
| 并发    | 线程是抢占式的，操作系统可以随时中断线程调度了一个线程 | 协程是协程式的，需要主动让出控制权时，才会进行任务切换 |
| 开销    | 创建线程和销毁线程，造成很大的开销           | 基于单线程的，并且协程是轻量级的，不会消耗大量资源。  |

协程的优势在于能够更高效地利用系统资源，在执行多个任务时能够充分利用CPU的性能。相比之下，并发执行的多个协程可以在单个线程内非阻塞地交替执行，从而减少了线程切换和上下文切换的开销，提高了整体的执行效率。

所以协程本身并不会直接提升单个任务的运行时间，但是，如果一个任务可以分解为多个步骤，并且这些步骤之间存在依赖关系，那么使用协程来执行这些步骤会更快。因为在等待I/O操作或其他异步操作完成时，协程可以让出CPU控制权，允许其他协程继续执行，从而最大程度地减少了等待时间。

  


例如从网站下载页面内容，并且计算页面内容。这就是单任务多步骤，这种情况就可以体现出协程的优势（性能、运行时间都会提升）。

```
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
```

> 内容长度为: [1256, 1256, 1256, 1256, 1256, 1256, 1256, 1256, 1256, 1256]
>
> 使用协程时间为: 0.5775842666625977 秒
>
> 内容长度为: [1256, 1256, 1256, 1256, 1256, 1256, 1256, 1256, 1256, 1256]
>
> 使用多线程时间为: 5.595600128173828 秒

可以看到这里的协程的运行时间提升了很多，因为是单任务多步骤，类似于流水线的方式，所以协程的速度会快很多。并且这里使用协程是单线程的，开销更小；而多线程这里使用了10个线程，开销更大。

# 三、多进程

如果任务主要由 CPU 运算组成（CPU密集型任务），而不涉及太多的 I/O 操作，那么多进程通常比多线程更适合，因为多进程能够利用多核处理器的全部性能，每个进程独立运行在自己的地址空间中，避开了 GIL 的限制。

例如大规模的计算，这种耗时的计算也是CPU密集型任务，使用多进程能明显的提升性能。

这里举例计算大规模积分

```
import multiprocessing
import threading
import numpy as np
import time

def integrate(f, a, b, N):
    """使用梯形法则计算f在区间[a, b]上的积分,N为分割数"""
    x = np.linspace(a, b, N)
    y = f(x)
    dx = (b - a) / (N - 1)
    return np.trapz(y, dx=dx)

def f(x):
    '''计算积分'''
    return np.sin(x) * np.exp(-x)

def integrate_range(start, end, result, index):
    result[index] = integrate(f, start, end, 100000000) 

def thread_main():
    result = [None] * 4
    threads = []
    ranges = [(0, 5), (5, 10), (10, 15), (15, 20)]  

    start_time = time.time()

    for i, (start, end) in enumerate(ranges):
        thread = threading.Thread(target=integrate_range, args=(start, end, result, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"多线程使用时间为: {end_time - start_time} 秒")
    print(f"积分结果: {result}\n")
def multiprocess_main():
    manager = multiprocessing.Manager()
    result = manager.list([None] * 4)
    processes = []
    ranges = [(0, 5), (5, 10), (10, 15), (15, 20)]  
    start_time = time.time()

    for i, (start, end) in enumerate(ranges):
        process = multiprocessing.Process(target=integrate_range, args=(start, end, result, i))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    end_time = time.time()
    print(f"多进程使用时间为: {end_time - start_time} 秒")
    print(f"积分结果: {result}")

if __name__ == "__main__":
    thread_main()    
    multiprocess_main()    
```

> 多线程使用时间为: 7.396134853363037 秒
>
> 积分结果: [0.5022749400837572, -0.0022435439294056455, -3.1379421486677834e-05, -1.809428816655182e-08]
>
>   
>
>
> 多进程使用时间为: 4.97518515586853 秒
>
> 积分结果: [0.5022749400837572, -0.0022435439294056455, -3.1379421486677834e-05, -1.809428816655182e-08]

可以看到这里的区别还是很大的，如果数据量更大，那么进程的优势会更明显。因为如果计算的时间过快，那么线程可以很快的进行切换。所以在大规模计算时，才可以体现出进程的优势。

  


# 四、总结

| 特性   | 进程       | 线程      | 协程         |
| ---- | -------- | ------- | ---------- |
| 创建开销 | 大        | 小       | 极小         |
| 切换开销 | 大        | 小       | 极小         |
| 内存共享 | 不共享      | 共享      | 共享         |
| 通信方式 | 管道、队列等   | 共享内存    | 直接调用       |
| 多核利用 | 是        | 受GIL影响  | 否          |
| 使用场景 | CPU密集型任务 | IO密集型任务 | 高并发IO密集型任务 |
| 复杂度  | 较高       | 较低      | 依赖异步编程。较高  |

## 1、进程（Process）

-   定义：进程是操作系统分配资源和调度的基本单位。每个进程拥有独立的内存空间、文件描述符和其他资源。

-   优点：

    -   独立性：进程之间相互独立，不会直接影响彼此的运行，崩溃一个进程不会影响其他进程。
    -   利用多核：能够充分利用多核 CPU 的优势，每个进程可以在不同的 CPU 核心上并行运行。

-   缺点：

    -   开销大：进程创建和销毁的开销较大，包括内存空间、文件句柄等资源。
    -   通信复杂：进程间通信（IPC）比较复杂，常用的 IPC 机制包括管道、消息队列、共享内存等。

-   使用场景：

    -   CPU 密集型任务，计算量大且需要充分利用多核 CPU 性能。
    -   需要高可靠性的任务，进程隔离可以防止任务间相互影响。

## 2、线程（Thread）

-   定义：线程是进程中的一个执行流，是 CPU 调度和执行的基本单位。线程共享进程的内存和资源。

-   优点：

    -   轻量级：创建和销毁线程的开销较小，线程之间的上下文切换开销比进程小。
    -   共享内存：同一进程的线程共享内存和资源，数据交换和通信更方便。

-   缺点：

    -   GIL 限制：在 Python 中，由于全局解释器锁（GIL），多线程在同一时间只能有一个线程执行 Python 字节码，限制了多线程在 CPU 密集型任务中的性能提升。
    -   线程安全：共享数据时需要小心处理线程同步问题，避免数据竞争、死锁等问题。

-   使用场景：

    -   I/O 密集型任务，如文件读写、网络请求等，可以在等待 I/O 完成时切换线程，提升效率。
    -   任务之间需要频繁的数据共享和通信的场景。

## 3、协程（Coroutine）

-   定义：协程是一种更轻量级的并发执行方式，协程在用户空间内实现切换，由程序自身控制，不依赖操作系统的调度。

-   优点：

    -   极轻量：协程的创建和切换开销极小，适合大量并发任务。
    -   无锁编程：协程之间通常不需要锁机制，因为协程在同一个线程中执行，不存在多线程的竞争问题。
    -   高效利用 I/O 等待：协程特别适合 I/O 密集型任务，可以在 I/O 等待时切换到其他协程执行。

-   缺点：

    -   单线程限制：协程在单线程中执行，无法利用多核 CPU 的优势。
    -   需要异步编程支持：需要语言和框架的异步支持，编写异步代码较为复杂。

-   使用场景：

    -   高并发的 I/O 密集型任务，如大量的网络请求处理、Web 服务器等。
    -   需要大量并发但任务之间独立性较高的场景。