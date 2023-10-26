import asyncio


async def exec_request_async(cursor, query, *params):
    loop = asyncio.get_event_loop()
    res = await loop.run_in_executor(
        None, lambda: cursor.execute(query, params))
    return res


async def read_async(file) -> str:
    loop = asyncio.get_event_loop()
    res = await loop.run_in_executor(None, file.read)
    return res
