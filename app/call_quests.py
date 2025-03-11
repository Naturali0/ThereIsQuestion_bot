from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from question_types import OpenQuestion, PollQuestion, InineKeyboardQuestion
from app.database.requests import get_next_user_question

router = Router()


async def send_poll_question(bot:Bot,chat_id,question:PollQuestion):
    bot.send_poll(chat_id=chat_id,
                  question = question.question,
                  allows_multiple_answers=True,
                  )


async def send_question(bot:Bot,user_id, delay):
    question = await get_next_user_question(user_id)
    await bot.send_message(user_id,question)
