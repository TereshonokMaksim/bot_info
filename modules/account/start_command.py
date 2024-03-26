from aiogram import types
from modules.data_work import edit_database
import aiogram.fsm.context as context
from modules.all_states import BasicStates
from modules.keyboards import admin_or_client_keyboard
import modules.new_message as new_message

restarted = False

async def start(message: types.Message, state: context.FSMContext):
    global restarted
    if message.chat.type == "private" and await state.get_state() == None:
        data = {'Past_State': BasicStates.starting, "Past_Message": ["Hi, user! Choose admin or client.", admin_or_client_keyboard], "Chat_History": [message.message_id]}
        data["Past_Data"] = data
        await state.set_data(data)
        edit_database(command = "CREATE TABLE IF NOT EXISTS admin_table (login TEXT, password TEXT, email TEXT, phone_number INTEGER, chat_id INTEGER, user_id INTEGER, aplication TEXT, info TEXT, message TEXT)")
        edit_database(command = "CREATE TABLE IF NOT EXISTS client_table (login TEXT, password TEXT, email TEXT, phone_number INTEGER, chat_id INTEGER, user_id INTEGER, info TEXT)")
        edit_database(command = "CREATE TABLE IF NOT EXISTS data (group_id TEXT, channel_id TEXT)")
        edit_database(command = "CREATE TABLE IF NOT EXISTS products (username TEXT, products TEXT)")
        if not restarted:
            restarted = True
            clients = ["client", "admin"]
            name_column = ["user", "chat"]
            for client in clients:
                for column in name_column:
                    edit_database(command = f"UPDATE {client}_table SET {column}_id = 0")
        await new_message.answer(text = "Hi, user! Choose admin or client.\nPlease note: If you want to cancel your action just use /cancel.", reply_markup = admin_or_client_keyboard, message = message, state = state) 
        print(await state.get_data())
        await state.set_state(BasicStates.starting)