import aiogram
import aiogram.types as types
import aiogram.filters as filters
import aiogram.methods as methods
from aiogram.fsm import context, state
from aiogram.fsm.storage.base import StorageKey
from modules.all_states import BasicStates
from modules.keyboards import admin_or_client_keyboard
from modules.data_work import edit_database

async def leave_account(message: types.Message, state: context.FSMContext):
    await message.answer(text = "You leaved your account")
    await message.answer(text = "Hi, user! Choose admin or client", reply_markup = admin_or_client_keyboard) 
    data = await state.get_data()
    edit_database(f"UPDATE {data['User']}_table SET user_id = 0 WHERE login = '{data['LogIn']}'")
    edit_database(f"UPDATE {data['User']}_table SET chat_id = 0 WHERE login = '{data['LogIn']}'")
    await state.set_data({})
    await state.set_state(BasicStates.starting)

async def kick_from_account(chat_id: int, dp: aiogram.Dispatcher = None, bot: aiogram.Bot = None, user_id: int = None):
    await bot.send_message(chat_id = chat_id, text = "You was kicked out of your account.\nFor create or enter in new account use /start.")
    state = context.FSMContext(
        storage = dp.storage,
        key = StorageKey(bot_id = bot.id, chat_id = chat_id, user_id = user_id)
    )
    await state.set_state(BasicStates.starting)
    await state.set_data({})