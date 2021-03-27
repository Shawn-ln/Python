from multiprocessing import Process, Pool
import time, os, random


def run(num):
    print("子进程%d启动---%s" % (num, os.getpid()))
    start = time.time()
    time.sleep(random.choice([1, 2, 3]))
    end = time.time()
    # print(end)
    print("子进程%d结束---%s---耗时%.2f" % (num, os.getpid(), end - start))


if __name__ == "__main__":
    print("父进程启动")
    # 创建进程池,Pool默认为CPU核心数
    pp = Pool()
    for i in range(8):
        # 创建进程，放入进程池统一管理
        result = pp.apply_async(run, args=(i,))
        # 进程池在调动join之前必须先调动close，调用close之后就不能再继续添加新的进程了
    pp.close()
    pp.join()
    print("父进程结束")
