import aiogram
import aiogram.types as types
import aiogram.filters as filters
from aiogram.fsm import context
from modules.all_states import BasicStates
from modules.data_work import edit_database, find_path
from modules.correct_data_checker import check_phone_number, check_email
import modules.new_message as new_message

async def registration_(message: types.Message, state: context.FSMContext, bot: aiogram.Bot, dp: aiogram.Dispatcher):
    data = await state.get_data()
    data_keys = list(data)
    if "EMail" in data_keys:
        if "Phone_Number" in data_keys:
            if "LogIn" in data_keys:
                if "Password" in data_keys:
                    print("You are arleady registred")
                else:
                    command = f"INSERT INTO {data['User'].lower()}_table (login, password, email, phone_number, user_id, chat_id) VALUES ('{data['LogIn']}', '{message.text}', '{data['EMail']}', {data['Phone_Number']}, {message.from_user.id}, {message.chat.id})"
                    edit_database(command)
                    # print(data)
                    if data["User"] == "admin":
                        print("what")
                        data_ = edit_database("SELECT chat_id FROM admin_table WHERE application = 'TheRealOwner0'")
                        print(f'{data_}\n\n{edit_database("SELECT chat_id FROM admin_table")}')
                        await state.set_state(BasicStates.application)
                        edit_database(f"UPDATE admin_table SET info = 'Not_verified' WHERE login = '{data['LogIn']}'")
                        add_text = "\nBut, that doesn't means that you arleady have all functional which administrators have.\nYou need to wait for your verify by administrators to have all functional.\nWe will message you when this will happen.\nAlso, you can write a application under this message to describe why you want to be administrator. This will increase your chances for administrator!"
                        # try:
                        chat_id = edit_database(command = "SELECT chat_id FROM admin_table")[0][0]
                        print(chat_id)
                        if chat_id != 0:
                            await new_message.send_message(chat_id = chat_id, text = f"There is a new application from {data['LogIn']}.\nHis username is {message.from_user.username}. Go to verification page to verificate him (logical).", dp = dp, bot = bot)
                        # except Exception as error:
                        #     print(error)
                    else:
                        await state.set_state(BasicStates.awaiting)
                        add_text = " "
                        data["Past_State"] = BasicStates.awaiting
                        data["Past_Message"] = ["You are registered.", None]
                        data["Past_Data"] = data
                    data.update({"Password": message.text})
                    await state.set_data(data)
                    print(command)
                    await new_message.clean_chat_history(state, bot, message.chat.id)
                    await new_message.answer(text = f"Registration successfull! If you want to leave your account use /leave. \nFor watching your profile use /profile.{add_text}", message = message, state = state)
            else:
                logins_raw = edit_database(command = "SELECT login FROM admin_table")
                logins = []
                for login in logins_raw:
                    logins.append(login[0])
                if message.text not in logins:
                    await new_message.answer(text = "Enter your new password: ", message = message, state = state)
                    await state.update_data({"LogIn": message.text})
                else:
                    await new_message.answer(message = message, text = "This login is arleady used by someone. \nPlease, use another one: ", state = state)
        else:
            if message.text.lower() != "skip":
                number = check_phone_number(message.text)
                if number != 0:
                    await state.update_data({"Phone_Number": number})
                    await new_message.answer(text = "Enter your new LogIn: ", message = message, state = state)
                else:
                    await new_message.answer(text = "Your phone number is invalid.", message = message, state = state)
            else:
                await state.update_data({"Phone_Number": 0})
                await new_message.answer(text = "Enter your new LogIn: ", message = message, state = state)
    else:
        succeful_mes = new_message.answer(text = "Enter your new phone number (like 012 345 6789 or 'Skip' if you don't want to): ", message = message, state = state)
        if message.text.lower() != "skip":
            email = check_email(message.text)
            if email != 0:
                await succeful_mes
                await state.update_data({"EMail": email})
            else:
                await new_message.answer(text = "Your E-Mail is invalid.", message = message, state = state)
        else:
            await succeful_mes
            await state.update_data({"EMail": "Absent"})