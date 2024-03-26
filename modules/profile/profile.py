import aiogram
from aiogram import Dispatcher, Bot, types
from modules.data_work import edit_database
from aiogram.fsm import context
from modules.all_states import SendStates, AdminStates, BasicStates
import modules.new_message as new_message
from modules.keyboards import profile_keyboard, keyboard_changes, button_names
from modules.account import leave_account
from modules.send_tools_message import send_admin_tools_message
from modules.correct_data_checker import check_phone_number, check_email

def get_prof_info(state_data: dict): 
        user_information = edit_database(command = f"SELECT * FROM {state_data['User']}_table WHERE login = '{state_data['LogIn']}'")[0]
        additional_text = ""
        if state_data["User"] == "admin":
            additional_text = f"\nYour admin information\nYou was verificated: {user_information[4]}\nYou are Good!"
        return f"Your profile:\nYour login: {state_data['LogIn']}\nYour password: {user_information[1]}\nYour phone number: {user_information[3]}\nYour email: {user_information[2]}\n{additional_text}"

async def open_profile(message: types.Message, state: context.FSMContext, bot: Bot):
    if await state.get_state() in [AdminStates.admin_awaiting, AdminStates.send_new_message, AdminStates.verif_page, SendStates.time, SendStates.image, SendStates.description, SendStates.edit, BasicStates.awaiting, BasicStates.application]:
        information = await state.get_data()
        message_text = get_prof_info(information)
        await new_message.clean_chat_history(state, bot = bot, chat_id = message.chat.id)
        msg = await new_message.answer(message = message, text = message_text, state = state, reply_markup = profile_keyboard)      
        information["Edit_Message_ID"] = msg.message_id
        information["Past_Message"] = [message_text, profile_keyboard]
        information["Past_State"] = BasicStates.profile
        information["Past_Data"] = information  
        await state.set_state(BasicStates.profile)
        await state.set_data(information)

async def change_acc_info(message: types.Message, state: context.FSMContext, bot: Bot):
    data = await state.get_data()
    if "New_Data_Message" in list(data):
        correct = False
        text = message.text
        if "password" not in data["New_Data_Message"][1][0]:
            if "phone_number" in data["New_Data_Message"][1][0]:
                phone_num = check_phone_number(text)
                if phone_num != 0: 
                    correct = True
                    text = phone_num
            else:
                email = check_email(text)
                if email != 0:
                    correct = True
                    text = email
        else:
            correct = True
        if correct:
            await new_message.delete_messages(messages_id = data["Chat_History"][data["Chat_History"].index(data["New_Data_Message"][0]):], chat_id = message.chat.id, state = state, bot = bot)
            edit_database(command = f"UPDATE {data['User']}_table SET {data['New_Data_Message'][1][0]} = '{message.text}' WHERE login = '{data['LogIn']}'")
            data[data["New_Data_Message"][1][1]] = message.text
            del data['New_Data_Message']
            await state.set_data(data)
            message_text = get_prof_info(data)
            try:
                await bot.edit_message_text(text = message_text, chat_id = message.chat.id, message_id = data["Edit_Message_ID"], reply_markup = profile_keyboard)
            except:
                print("Edit message not found")
        else:
            print(data["Chat_History"][data["Chat_History"].index(data["New_Data_Message"][0]):])
            await new_message.answer(text = f"Incorrect {data['New_Data_Message'][1][1]}!", state = state, message = message)
        
async def callback_profile(callback: types.CallbackQuery, state: context.FSMContext, bot: Bot):
    if await state.get_state() == BasicStates.profile:
        data = await state.get_data()
        text = callback.data.lower()
        if "Message_ID" not in list(data):
            if text == profile_keyboard.inline_keyboard[1][0].callback_data:
                await leave_account(message = callback.message, state = state, bot = bot)
            elif text == profile_keyboard.inline_keyboard[2][0].callback_data:
                await new_message.clean_chat_history(state = state, bot = bot, chat_id = callback.message.chat.id)
                del data["Edit_Message_ID"]
                await state.set_data(data)
                if data["User"] == "admin":
                    await send_admin_tools_message(message = callback.message, state = state, user_id = callback.from_user.id)
                else:
                    await state.set_state(BasicStates.awaiting)
            elif text == profile_keyboard.inline_keyboard[0][0].callback_data:
                message_text = f"What would you like to change: "
                msg = await new_message.answer(message = callback.message, text = message_text, reply_markup = keyboard_changes, state = state)
                data["Message_ID"] = msg.message_id
                await state.set_data(data)
        elif "New_Data_Message" not in list(data):
            if "change" in text:
                if "close" in text:
                    await new_message.delete_messages(messages_id = [data["Message_ID"]], chat_id = callback.message.chat.id, state = state, bot = bot)
                    del data["Message_ID"]
                    await state.set_data(data)
                else:
                    change_name = text.split("_")[1]
                    change_name = change_name.split(" ")
                    change_name = " ".join([proc_name[0].capitalize() + proc_name[1:] for proc_name in change_name])
                    msg = await new_message.answer(message = callback.message, text = f"Enter your new {change_name}: ", state = state)
                    data["New_Data_Message"] = [msg.message_id, button_names[change_name]]
                    await state.set_data(data)
        await callback.answer("")
