import asyncio

import requests

import pandas as pd
import numpy as np


# from


# async def count():
#     print("One")
#     await asyncio.sleep(1)
#     print("Two")

# async def main():
#     await asyncio.gather(count(), count(), count())


# L = list()


# # async
# async def async_funct(url: str):
#     """ """

#     try:
#         print(url)
#         res = await requests.get(url)

#         if res.status_code < 300:
#             L.append((url, res.text))
#         else:
#             L.append((url, res.status_code))
#         return None

#     except Exception as e:
#         L.append((url, str(e)))
#         return None


# async def bulk_crawl(df, col):
#     """ """

#     tasks = [async_funct(url) for url in df[col].values]

#     await asyncio.gather(*tasks)


# # run

# asyncio.run(bulk_crawl(_df, "press_release_URL"))
