import asyncio
from abc import abstractmethod, ABC
from sqlite3 import Connection
from typing import TypeVar, Generic, List

T = TypeVar('T')


class Parameter(ABC):
    @abstractmethod
    def get_parameter_to_sync(self):
        pass


class BuiltInParameter(Parameter):

    def __init__(self, value):
        self.__value = value

    def get_parameter_to_sync(self):
        return str(self.__value)


class Query:

    def __init__(self, path: str, sql_request: str = ""):
        self.__path: str = path
        self.__sql_request: str = sql_request

    async def get_sql_request_async(self) -> str:
        if self.__sql_request:
            return self.__sql_request

        with open(self.__path) as file:
            loop = asyncio.get_event_loop()
            res = await loop.run_in_executor(None, file.read)
            self.__sql_request = res

        return self.__sql_request


class Request:
    PLACE_HOLDER = "?"

    def __init__(self, query: Query, params: List[Parameter]):
        self.__query: Query = query
        self.__request: str = ""
        self.__params: List[Parameter] = params

    async def get_request_async(self) -> str:
        if self.__request:
            return self.__request

        query = await self.__query.get_sql_request_async()
        parts = query.split(self.PLACE_HOLDER)

        request_arr = []
        for i, val in enumerate(self.__params):
            request_arr.append(parts[i])
            request_arr.append(str(val.get_parameter_to_sync()))

        for i in range(len(self.__params), len(parts)):
            request_arr.append(parts[i])

        self.__request = "".join(request_arr)
        return self.__request

    def __str__(self):
        if self.__request:
            return self.__request


class DataBase:

    def __init__(self, db: Connection):
        self.__db: Connection = db

    async def execute_request(self, request: Request):
        request_content = await request.get_request_async()
        cursor = self.__db.cursor()

        loop = asyncio.get_event_loop()

        await loop.run_in_executor(None, lambda: cursor.execute(request_content))

        result = cursor.fetchall()
        cursor.close()

        self.__db.commit()

        return result

    def close(self):
        self.__db.close()


class SyncObject:
    def __init__(self, db: DataBase, sync_request: Request, flush_request: Request):
        self.__db = db
        self.__sync_request = sync_request
        self.__flush_request = flush_request

    @abstractmethod
    async def sync(self):
        pass

    async def get_sync_values(self):
        return await self.__db.execute_request(self.__sync_request)

    async def flush(self):
        await self.__db.execute_request(self.__flush_request)

    async def delete(self):
        await self.__db.execute_request(self.__delete_request)


class Field(Generic[T], Parameter, SyncObject):

    def __init__(self, value: T, synced: bool, db: DataBase = None, sync_request: Request = None,
                 flush_request: Request = None):
        super().__init__(db, sync_request, flush_request)
        self.__value = value
        self.synced = synced

    async def get_value(self):
        if self.synced:
            return self.__value

        await self.sync()

        return self.__value

    async def sync(self):
        value = await super().get_sync_values()
        self.__value = value
        self.synced = True

    def set_value(self, value):
        self.synced = value == self.__value
        self.__value = value

    def get_parameter_to_sync(self):
        self.synced = True
        return str(self.__value)
