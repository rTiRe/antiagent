import asyncio
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv('TOKEN')
AGENTS_IDS = list(map(int, getenv('AGENT_IDS').strip().split(',')))
DISCLAIMER = 'НАСТОЯЩИЙ МАТЕРИАЛ (ИНФОРМАЦИЯ) ПРОИЗВЕДЕН, РАСПРОСТРАНЕН И (ИЛИ) НАПРАВЛЕН ИНОСТРАННЫМ АГЕНТОМ АЛЕКСЕЕМ НЕГРОВИЧЕМ ЗАЙЦЕВЫМ ЛИБО КАСАЕТСЯ ДЕЯТЕЛЬНОСТИ ИНОСТРАННОГО АГЕНТА АЛЕКСЕЯ НЕГРОВИЧА ЗАЙЦЕВА'

async def delete_agent_message(message: Message) -> None:
    is_agent = message.from_user.id in AGENTS_IDS
    has_disclaimer = message.text.startswith(DISCLAIMER)
    if is_agent and not has_disclaimer:
        await message.answer(f'@{message.from_user.username} Вам запрещено отправлять сообщения без дисклеймера о том, что Вы являетесь иностранным агентом.')
        await message.delete()


async def main() -> None:
    dispatcher = Dispatcher()
    bot = Bot(token=TOKEN)
    dispatcher.message.register(delete_agent_message)
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
