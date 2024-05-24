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

