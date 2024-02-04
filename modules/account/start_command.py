from aiogram import types
from modules.data_work import edit_database
import aiogram.fsm.context as context
from modules.all_states import BasicStates
from modules.keyboards import admin_or_client_keyboard



async def start(message: types.Message, state: context.FSMContext):
    edit_database(command = "CREATE TABLE IF NOT EXISTS admin_table (login TEXT, password TEXT, email TEXT, phone_number INTEGRER)")
    edit_database(command = "CREATE TABLE IF NOT EXISTS client_table (login TEXT, password TEXT, email TEXT, phone_number INTEGRER)")
    edit_database(command = "CREATE TABLE IF NOT EXISTS data (group_id TEXT, channel_id TEXT)")
    await message.answer(text = "Hi, user! Choose admin or client", reply_markup = admin_or_client_keyboard) 
    await state.set_state(BasicStates.starting)