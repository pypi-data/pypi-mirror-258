# -*- coding: utf-8 -*-
# @time: 2022/4/21 16:50
# @author: Dyz
# @file: time.py
# @software: PyCharm
import asyncio
from functools import wraps
from time import gmtime, strftime, time


def timer(func):
    """ 计算时间装饰器 """
    if asyncio.iscoroutinefunction(func):
        @wraps(func)
        async def aio_wrapper(*args, **kwargs):
            start_time = time()
            res = await func(*args, **kwargs)
            time_ = strftime("%H:%M:%S", gmtime(time() - start_time))
            print(f'{func.__name__} 耗时: {time_}')
            return res

        return aio_wrapper

    else:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time()
            res = func(*args, **kwargs)
            time_ = strftime("%H:%M:%S", gmtime(time() - start_time))
            print(f'{func.__name__} 耗时: {time_}')
            return res

        return wrapper
