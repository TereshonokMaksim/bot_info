import aiogram
from aiogram import types
from aiogram.fsm import context
from modules.data_work import edit_database
from modules.all_states import BasicStates

async def application_checker(message: types.Message, state: context.FSMContext):
    if await state.get_state() == BasicStates.application:
        data = await state.get_data()
        edit_database(f"UPDATE admin_table SET application = '{message.text}' WHERE login = '{data['LogIn']}'")
        await message.answer(text = "Your application was saved! Now, wait until you will be accepted as administrator.\nSee you later!")
        await state.set_state(BasicStates.awaiting)