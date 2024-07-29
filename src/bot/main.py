import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import CommandStart
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.base import DefaultKeyBuilder
from redis.asyncio.client import Redis
from aiogram_dialog import setup_dialogs

from src.bot.dialogs.request_mark import mark_dialog

bot = Bot(token="7212842882:AAFkZ5ZD5asu6R1REXmzFYDOpaSWqv_BkOQ")
redis_client = Redis(host='87.242.101.16')
storage = RedisStorage(redis=redis_client, key_builder=DefaultKeyBuilder(with_destiny=True))

dp = Dispatcher(storage=storage)
dp.include_router(mark_dialog)
bg_manager = setup_dialogs(dp)


@dp.message(CommandStart())
async def get_contact(message: types.Message):
    await message.answer(f"Здравствуйте👋\n\nБлогодарим за проявленное доверие нашей компании.\n\n"
                         f"🔔 Здесь будут появляться уведомления по вашим заказам\n\n"
                         f"Пожалуйста, назовите этот код сотруднику: {message.from_user.id}")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
