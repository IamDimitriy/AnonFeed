from Types import User

Users = []


async def get_user_by_uid(uid: str) -> User:
    for user in Users:
        if user.get_uid() == uid:
            return user

    return User()


async def get_user_by_telegram_uid(telegram_uid: int) -> User:
    for user in Users:
        if user.get_telegram_uid() == telegram_uid:
            return user

    return User()


async def get_user_uid(telegram_uid: int) -> str:
    for user in Users:
        if user.get_telegram_uid() == telegram_uid:
            return user.get_uid()

    return ""
