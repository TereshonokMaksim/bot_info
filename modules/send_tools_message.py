from aiogram import types
from aiogram.fsm import context
from modules.data_work import edit_database
from modules.keyboards import admin_uncomplete_keyboard, admin_keyboard
import modules.new_message as new_message
from .all_states import AdminStates

async def send_admin_tools_message(message: types.Message | types.CallbackQuery, state: context.FSMContext, user_id: int):
    
    data = await state.get_data()
    if isinstance(message, types.CallbackQuery):
        message = message.message

    if user_id == int(edit_database(command = "SELECT user_id FROM admin_table")[0][0]) and data["LogIn"] == edit_database(command = "SELECT login FROM admin_table")[0][0]:
        await new_message.answer(text = f"What you want to do, Owner?", reply_markup = admin_keyboard, message = message, state = state) 
        markup = admin_keyboard
    else:
        await new_message.answer(text = f"Do you want to send a new message?", reply_markup = admin_uncomplete_keyboard, state = state, message = message)
        markup = admin_uncomplete_keyboard
    data["Past_State"] = AdminStates.admin_awaiting
    data["Past_Message"] = ["You are authorized as administrator", markup]
    data["Pas_Data"] = data
    await state.set_state(AdminStates.admin_awaiting)
    await state.set_data(data = data)