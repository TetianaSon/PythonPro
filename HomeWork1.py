# Декоратор сache з підтримкою max_limit.
# Алгоритм кешування LFU: https://en.wikipedia.org/wiki/Least_frequently_used

import functools
import time
from collections import OrderedDict
import requests


def profile(f):
    def internal(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        print(f'Elapsed time: {time.time() - start}ms')
        return result
    return internal


def cache(max_limit=5):
    def internal(f):
        @functools.wraps(f)
        def deco(*args):
            if args in deco._cache:
                deco.counter[args] += 1
                print(deco.counter)
                return deco._cache[args]
            result = f(*args)
            deco.counter[args] = 0
            deco._cache[args] = result
            # видалення зі словника лічильників значення, у якого найменша кількість використань
            if len(list(deco.counter.keys())) > max_limit:
                for key in list(deco.counter.keys()):
                    if deco.counter[key] == min(list(deco.counter.values())):
                        del deco.counter[key]
                        del deco._cache[key]
                        break
            print(deco.counter)
            return result

        deco._cache = OrderedDict()
        deco.counter = OrderedDict()
        return deco
    return internal


@profile
@cache(max_limit=6)
def fetch_url(url, first_n=100):
    """Fetch a given url"""
    res = requests.get(url)
    return res.content[:first_n] if first_n else res.content


fetch_url('https://google.com')
fetch_url('https://google.com')
fetch_url('https://google.com')
fetch_url('https://youtube.com')
fetch_url('https://youtube.com')
fetch_url('https://dou.ua')
fetch_url('https://en.wikipedia.org')
fetch_url('https://duckduckgo.com')
fetch_url('https://apple.com')
fetch_url('https://www.python.org')
fetch_url._cache
