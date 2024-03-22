import asyncio
from datetime import datetime
from typing import TextIO

import Utils


class Conversion:

    def __init__(self, file: TextIO):
        self.__file: TextIO = file

    def count_answer(self, ):
        now = datetime.now()
        asyncio.create_task(
            Utils.write_async(self.__file, str(now) + "answer\n"))

    def count_link_follow(self):
        now = datetime.now()
        asyncio.create_task(
            Utils.write_async(self.__file, str(now) + "link\n"))
