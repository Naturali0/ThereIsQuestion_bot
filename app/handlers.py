from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from app.database.requests import add_new_user, get_user, delete_user, is_registered, get_next_user_question, update_unswered_questions
from school_proj.app import question_types
from school_proj.app.call_quests import send_question


router = Router()

questions = {
            "Питання":"відповідь"
            }

class Reg(StatesGroup):
    name = State()
    number = State()

class QuestinState(StatesGroup):
    question = State()
    answer = State


class UserInfo(StatesGroup):
    category = State()

@router.message(CommandStart())
async def cmd_start(message:Message):
    await message.reply("Дового дня, оберіть ваш клас",reply_markup=await kb.user_categories_keyboard())


@router.message(Command("start_test"))
async def start_test(message: Message,state:FSMContext):

    question = await get_next_user_question(message.from_user.id)
    
    await state.update_data(question=question)

    await message.answer(question)
    state.set_state(QuestinState.answer)

    pass



@router.message(QuestinState.answer)
async def answer_handler(message: Message, state:FSMContext): 
    data = await state.get_data()

    await update_unswered_questions(message.from_user.id,data["question"],message.text)    

    await message.answer("Say your name")



@router.message(Command("get_me"))
async def get_self(message: Message):
    if not is_registered(message.from_user.id):
        await message.answer("Вы небыли зарегестрированы что б совершить выбранную операцию")

    user = await get_user(message.from_user.id) 
    await message.answer(f"tg_id= {user.tg_id} name={user.name}")


@router.message(Command("unreg"))
async def unreg(message:Message):
    if not is_registered(message.from_user.id): 
        await message.answer("Вы небыли зарегестрированы что б совершить выбранную операцию")

    user = await get_user(message.from_user.id) 
    await delete_user(user)
    await message.answer("Вы удалены")



@router.message(Command("reg"))
async def reg_one(message: Message, state:FSMContext): 
    await state.set_state(Reg.name)
    await message.answer("Say your name")


@router.message(Reg.name)
async def reg_two(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    #await state.set_state(Reg.number)
    data = await state.get_data()
    await add_new_user(tg_id=message.from_user.id, name=data['name'])

    await message.answer("Ты добавлен")


@router.callback_query(F.text.startswith("category_"))
async def category_selected(message: Message, state:FSMContext):
    user_category = message.data.split("_")[1]

    await add_new_user(message.from_user.id,message.from_user.first_name,user_category,list(questions.keys()))
    await message.answer(f"Вы выбрали категорию {user_category}")
    #state.update_data()

    
#@router.message(Reg.number)
#async def reg_three(message: Message, state: FSMContext):
#    await state.update_data(number=message.text)
#    data = await state.get_data()
#    await message.answer(f"ok {data['name']=} {data['number']=}")
#    await state.clear()



