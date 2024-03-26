import aiogram
from aiogram import types
from aiogram.fsm import context
from modules.data_work import edit_database
from modules.all_states import BasicStates
import modules.new_message as new_message

async def application_checker(message: types.Message, state: context.FSMContext, bot: aiogram.Bot):
    # if await state.get_state() == BasicStates.application:
    data = await state.get_data()
    await new_message.clean_chat_history(state, bot, message.chat.id)
    edit_database(f"UPDATE admin_table SET application = '{message.text}' WHERE login = '{data['LogIn']}'")
    await new_message.answer(text = "Your application was saved! Now, wait until you will be accepted as administrator.\nSee you later!", message = message, state = state)
    await state.set_state(BasicStates.awaiting)