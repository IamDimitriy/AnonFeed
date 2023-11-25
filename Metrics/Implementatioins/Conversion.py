import asyncio
from datetime import datetime
from typing import TextIO

import Utils


class Conversion:

    def __init__(self, file: TextIO):
        self.__file: TextIO = file

    def count_answer(self, func):
        def wrapper(*args,**kwargs):
            res = func(*args,**kwargs)
            now = datetime.now()
            asyncio.create_task(
                Utils.write_async(self.__file, str(now) + "answer\n"))
            return res

        return wrapper

    def count_link_follow(self, func):
        def wrapper(*args,**kwargs):
            res = func(*args,**kwargs)
            now = datetime.now()
            asyncio.create_task(
                Utils.write_async(self.__file, str(now) + "link\n"))
            return res

        return wrapper
