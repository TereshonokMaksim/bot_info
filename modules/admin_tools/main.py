import aiogram
from aiogram import types, filters, exceptions
from aiogram.fsm import context
from modules.data_work import edit_database
from modules.messages import send_message, send_edit_message, add_func
from modules.all_states import AdminStates, BasicStates
from modules.keyboards import admin_keyboard, verif_page_keyboard, open_send_page, edit_message_keyboard
import modules.new_message as new_message
from ..send_tools_message import send_admin_tools_message

# from .verificate import 


async def open_main_admin_tools(message: types.Message, state: context.FSMContext):
    data = await state.get_data()
    if data["User"].lower() == "admin":
        if message.text.lower() == "/tools":
            data["Past_State"] = AdminStates.admin_awaiting
            data["Past_Data"] = data
            await send_admin_tools_message(message = message, state = state, user_id = message.from_user.id)
            await state.set_data(data = data)


async def send_verif_page_message(message: types.Message, state: context.FSMContext):
    all_admins = edit_database("SELECT login FROM admin_table")
    all_verifs = edit_database("SELECT info FROM admin_table")
    unverifed_users = []
    user_text = ""
    bottom_text = ""
    for num in range(len(all_admins)):
        if "Not_verified" in all_verifs[num]:
            unverifed_users.append([all_admins[num]])
            # button = types.KeyboardButton(text = f"{len(unverifed_users)}. {all_admins[num][0]}")
            user_text = f"{user_text}\n{len(unverifed_users)}. {all_admins[num][0]}"
            bottom_text = "Send user login or number on the left of login to choose user."
    if len(unverifed_users) == 0:
        user_text = "\nThere is no applications now."
        bottom_text = "Check applications later."
    # data = await state.get_data()
    message = await new_message.answer(text = f"List of new applications: \n{user_text}\n\n{bottom_text}", reply_markup = verif_page_keyboard, message = message, state = state)
    # data["Verif_Message_ID"] = message.message_id
    # await state.set_data(data = data)
            
            
async def handle_admin_keyboard(callback: types.CallbackQuery, state: context.FSMContext, bot: aiogram.Bot):
    print("state: ", await state.get_state())
    if await state.get_state() == AdminStates.admin_awaiting:
        print("check callback: ", callback.data)
        if callback.data == "verif_page":
            try:
                await new_message.delete_messages(messages_id = [callback.message.message_id], chat_id = callback.message.chat.id, state = state, bot = bot)
            except Exception as error:
                print(error)
            await state.set_state(AdminStates.verif_page)
            await send_verif_page_message(message = callback.message, state = state)
        elif callback.data == "new_message":
            data = await state.get_data()
            chat_id = callback.message.chat.id
            # message_data = edit_database(command = f"SELECT message FROM admin_table WHERE login = '{data['LogIn']}'")

            data["Admin_Tools_ID"] = callback.message.message_id
            data["Past_State"] = AdminStates.send_new_message
            data["Past_Message"] = ["What do you want to do with this message?", edit_message_keyboard]
            data["Past_Data"] = data

            try:
                id_message = data['Message_ID']
                await new_message.delete_messages(chat_id = chat_id, messages_id = id_message, bot = bot, state = state)
                await new_message.delete_messages(chat_id = chat_id, messages_id = data["Edit_Message_ID"], bot = bot, state = state)
            except exceptions.TelegramBadRequest as error:
                print("that message arleady deleted")
            except KeyError as error:
                print(f"Admin {data['LogIn']} called first message")
            except Exception as error:
                print(f"Some error occured!\n{error}")

            try:
                await new_message.delete_messages(messages_id = [callback.message.message_id], chat_id = callback.message.chat.id, state = state, bot = bot)
            except Exception as error:
                print(error)

            new_func = open_main_admin_tools(message = callback.message, state = state)
            add_func(new_function = new_func)

            await state.set_data(data = data)

            await state.set_state(AdminStates.send_new_message)
            print("a")
            await send_message(state = state, message = callback, bot = bot, test = True)
            print("b")
            await send_edit_message(message = callback.message, state = state, bot = bot)
            