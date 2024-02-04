import aiogram
from aiogram import types, filters
from aiogram.fsm import context
from modules.data_work import edit_database
from modules.all_states import AdminStates, BasicStates
from modules.keyboards import admin_keyboard, verif_page_keyboard
# from .verificate import 

async def open_main_admin_tools(message: types.Message, state: context.FSMContext):
    data = await state.get_data()
    if await state.get_state() == AdminStates.admin_awaiting:
        if data["User"].lower() == "admin":
            if message.text.lower() == "/tools":
                await message.answer(text = f"Ok, what do you want to do now, {message.from_user.first_name}?", reply_markup = admin_keyboard)
        else:
            message.answer(text = "Wait, you are not administrator! You can't use administrator tools, don't use this command anymore!")

async def send_verif_page_message(message: types.Message):
    all_admins = edit_database("SELECT login FROM admin_table")
    all_verifs = edit_database("SELECT info FROM admin_table")
    unverifed_users = []
    user_text = ""
    bottom_text = ""
    for num in range(len(all_admins)):
        if "Not_verified" in all_verifs[num]:
            unverifed_users.append([all_admins[num]])
            button = types.KeyboardButton(text = f"{len(unverifed_users)}. {all_admins[num][0]}")
            user_text = f"{user_text}\n{len(unverifed_users)}. {all_admins[num][0]}"
            bottom_text = "Send user login or number on the left of login to choose user."
    if len(unverifed_users) == 0:
        user_text = "\nThere is no applications now."
        bottom_text = "Check applications later."
    await message.answer(f"List of new applications: \n{user_text}\n\n{bottom_text}", reply_markup = verif_page_keyboard)
            
            
async def handle_admin_keyboard(callback: types.CallbackQuery, state: context.FSMContext):
    print("state: ", await state.get_state())
    if await state.get_state() == AdminStates.admin_awaiting:
        print("check callback: ", callback.data)
        if callback.data == "verif_page":
            await state.set_state(AdminStates.verif_page)
            await send_verif_page_message(message = callback.message)
        elif callback.data == "new_message":
            await state.set_state(AdminStates.send_new_message)
            await callback.message.answer("Ok, then, send a message title.")
            
            