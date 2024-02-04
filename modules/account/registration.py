import aiogram
import aiogram.types as types
import aiogram.filters as filters
from aiogram.fsm import context
from modules.all_states import BasicStates
from modules.data_work import edit_database
import re


        
   

async def registration_(message: types.Message, state: context.FSMContext):
    data = await state.get_data()
    data_keys = list(data)
    if "EMail" in data_keys:
        if "Phone_Number" in data_keys:
            if "LogIn" in data_keys:
                if "Password" in data_keys:
                    print("You are arleady registred")
                else:
                    if data["User"] == "Admin":
                        await state.set_state(BasicStates.application)
                        additional_data = "Not_verified"
                        add_text = "\nBut, that doesn't means that you arleady have all functional which administrators have.\nYou need to wait for your verify by administrators to have all functional.\nWe will message you when this will happen.\nAlso, you can write a application under this message to describe why you want to be administrator. This will increase your chances for administrator!"
                    else:
                        await state.set_state(BasicStates.awaiting)
                        additional_data = " "
                        add_text = " "
                    command = f"INSERT INTO {data['User'].lower()}_table (login, password, email, phone_number, info, user_id, chat_id) VALUES ('{data['LogIn']}', '{message.text}', '{data['EMail']}', {data['Phone_Number']}, '{additional_data}', {message.from_user.id}, {message.chat.id})"
                    print(command)
                    edit_database(command)
                    await message.answer(text = f"Registration successfull! If you want to leave your account use /leave{add_text}")
                    await state.update_data({"Password": message.text})
            else:
                await message.answer(text = "Enter your new password: ")
                await state.update_data({"LogIn": message.text})
        else:
            if re.match(r"^\d{3}-\d{3}-\d{4}$", message.text) or re.match(r"^\d{3}\d{3}\d{4}$", message.text):
                await state.update_data({"Phone_Number": message.text})
                await message.answer(text = "Enter your new LogIn: ")
            elif message.text.lower() == "skip":
                await state.update_data({"Phone_Number": 0})
                await message.answer(text = "Enter your new LogIn: ")
            elif re.match(r"^\d{3} \d{3} \d{4}$", message.text):
                await state.update_data({"Phone_Number": "".join(message.text.split())})
                await message.answer(text = "Enter your new LogIn: ")
            else:
                await message.answer(text = "Your phone number is invalid.")
    else:
        if re.match(r"[^@]+@[^@]+\.[^@]+", message.text):  
            await message.answer(text = "Enter your new phone number (like 012 345 6789 or 'Skip' if you don't want to): ")
            await state.update_data({"EMail": message.text})
        elif message.text.lower() == "skip":
            await message.answer(text = "Enter your new phone number (like 012 345 6789 or 'Skip' if you don't want to): ")
            await state.update_data({"EMail": "Absent"})
        else:
            await message.answer(text = "Your E-Mail is invalid.")