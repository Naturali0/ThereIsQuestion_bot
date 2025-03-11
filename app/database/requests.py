from app.database.models import User, async_session
from sqlalchemy import select



async def add_new_user(tg_id,name,cls,remaining_questions):
    async with async_session() as session:
        new_user = User(tg_id=tg_id,name=name,cls=cls,questions=remaining_questions)
        session.add(new_user)
        await session.commit()


async def delete_user(user):
    async with async_session() as session:
        await session.delete(user)
        await session.commit()


async def get_user(tg_id):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.tg_id==tg_id))
        user = result.scalars().first()
        return user


async def is_registered(tg_id):
    user = await get_user(tg_id)
    return isinstance(user, User)


async def get_next_user_question(tg_id):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.tg_id==tg_id))
        user = result.scalars().first()

        question = user.remaining_questions.pop()
        await session.commit()
        return question


async def update_unswered_questions(tg_id,question,answer):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.tg_id==tg_id))
        user = result.scalars().first()

        user.answered_questions.setdefault(question,answer)
        await session.commit()
