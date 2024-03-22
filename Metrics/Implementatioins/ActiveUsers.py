import asyncio
from datetime import datetime
from typing import TextIO

import Utils


class ActiveUsers:
    def __init__(self, file: TextIO):
        self.__file: TextIO = file

    def mark_user(self, func):
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            now = datetime.now()
            asyncio.create_task(
                Utils.write_async(self.__file, str(now) + " " + str(args[1]) + "\n"))
            return res

        return wrapper
