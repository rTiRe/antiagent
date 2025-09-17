import asyncio
from os import getenv

from aiogram import F, Bot, Dispatcher
from aiogram.types import Message
from dotenv import load_dotenv
from aiogram_media_group import media_group_handler

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


async def check_needs_delete(messages: list[Message]) -> bool:
    is_agent = await check_is_agent(messages[0].from_user.id)
    has_disclaimer = False
    for message in messages:
        has_disclaimer = await check_has_disclaimer(message.text or message.caption or '')
        if has_disclaimer:
            break
    return is_agent and not has_disclaimer


async def delete_agent_messages(messages: list[Message]) -> None:
    if not await check_needs_delete(messages):
        return
    await messages[0].answer(f'@{messages[0].from_user.username}, Вам запрещено отправлять сообщения без дисклеймера о том, что Вы являетесь иностранным агентом.')
    for message in messages:
        await message.delete()


async def delete_agent_message(message: Message) -> None:
    await delete_agent_messages([message])


async def main() -> None:
    dispatcher = Dispatcher()
    bot = Bot(token=TOKEN)
    dispatcher.message.register(media_group_handler(delete_agent_messages), F.media_group_id)
    dispatcher.edited_message.register(media_group_handler(delete_agent_messages), F.media_group_id)
    dispatcher.message.register(delete_agent_message)
    dispatcher.edited_message.register(delete_agent_message)
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
