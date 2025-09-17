import asyncio
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv('TOKEN')
AGENTS_IDS = list(map(int, getenv('AGENT_IDS').strip().split(',')))
DISCLAIMERS = [
    'НАСТОЯЩИЙ МАТЕРИАЛ (ИНФОРМАЦИЯ) ПРОИЗВЕДЕН, РАСПРОСТРАНЕН И (ИЛИ) НАПРАВЛЕН ИНОСТРАННЫМ АГЕНТОМ АЛЕКСЕЕМ НЕГРОВИЧЕМ ЗАЙЦЕВЫМ ЛИБО КАСАЕТСЯ ДЕЯТЕЛЬНОСТИ ИНОСТРАННОГО АГЕНТА АЛЕКСЕЯ НЕГРОВИЧА ЗАЙЦЕВА',
]

async def check_is_agent(telegram_id: int) -> bool:
    return telegram_id in AGENTS_IDS


async def check_has_disclaimer(text: str = '') -> bool:
    if not isinstance(text, str):
        return False
    text = text.upper()
    has_disclaimer = False
    for disclaimer in DISCLAIMERS:
        has_disclaimer = text.startswith(disclaimer)
        if has_disclaimer:
            break
    return has_disclaimer


async def check_needs_delete(message: Message) -> bool:
    is_agent = await check_is_agent(message.from_user.id)
    has_disclaimer = await check_has_disclaimer(message.text or message.caption or '')
    return is_agent and not has_disclaimer


async def delete_agent_message(message: Message) -> None:
    if await check_needs_delete(message):
        await message.answer(f'@{message.from_user.username}, Вам запрещено отправлять сообщения без дисклеймера о том, что Вы являетесь иностранным агентом.')
        await message.delete()


async def main() -> None:
    dispatcher = Dispatcher()
    bot = Bot(token=TOKEN)
    dispatcher.message.register(delete_agent_message)
    dispatcher.edited_message.register(delete_agent_message)
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
