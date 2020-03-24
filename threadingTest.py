# -*- coding: utf-8 -*-
import threading,time


def lighter():
    num = 0
    event.set()     # 设置标记
    while True:
        if num >= 5 and num < 10:
            event.clear()    # 清除标记
            print("红灯亮起，车辆禁止通行")
        if num >= 10:
            event.set()     # 设置标记
            print("绿灯亮起，车辆可以通行")
            num = 0
        num += 1
        time.sleep(1)


def car():
    while True:
        if event.is_set():
            print("车辆正在跑...")
        else:
            print("车辆停下了")
            event.wait()
        time.sleep(1)


event = threading.Event()
t1 = threading.Thread(target=lighter,)
t2 = threading.Thread(target=car,)
t1.start()
t2.start()