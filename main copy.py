#PARKING SUPER FREE NO SCAM!!! skachat brawl stars bez virusov besplatno pro max no registration and sms or mms
import aiogram
from aiogram import filters, types 
from  aiogram.fsm import state, context
import asyncio
import sqlite3
import os
import re

def find_path(path: str):
    return os.path.abspath(__file__ + f"/../{path}")

def edit_database(command: str):
    with sqlite3.connect(find_path(path = "database.db")) as database:
        cursor = database.cursor()
        cursor.execute(command)
        data = cursor.fetchall()
        database.commit()
    return data

bot = aiogram.Bot(token = "6354577537:AAE92wOYz7o1VxA3r6f8ZoYmNnvy2nSlQsk")
dp = aiogram.Dispatcher()

admin_button = types.KeyboardButton(text = "Admin")
client_button =  types.KeyboardButton(text = "Client")
admin_or_client_keyboard = types.ReplyKeyboardMarkup(keyboard = [[admin_button, client_button]])

reg_button = types.KeyboardButton(text = "Registration")
autoris_button = types.KeyboardButton(text = "authorization")
registration_or_authorization_keyboard = types.ReplyKeyboardMarkup(keyboard = [[reg_button, autoris_button]])

delete_keyboard = types.ReplyKeyboardRemove()

class BasicStates(state.StatesGroup):
    starting = state.State()
    reg_or_auto = state.State()
    registration = state.State()
    authorization = state.State()
    awaiting = state.State()

@dp.message(filters.StateFilter(None), filters.CommandStart())

async def start(message: types.Message, state: context.FSMContext):
    edit_database(command = "CREATE TABLE IF NOT EXISTS admin_table (login TEXT, password TEXT, email TEXT, phone_number INTEGRER)")
    edit_database(command = "CREATE TABLE IF NOT EXISTS client_table (login TEXT, password TEXT, email TEXT, phone_number INTEGRER)")
    await message.answer(text = "Hi, user! Choose admin or client", reply_markup = admin_or_client_keyboard) 
    await state.set_state(BasicStates.starting)

@dp.message()

async def enter(message: types.Message, state: context.FSMContext):
    state_type = await state.get_state()
    if state_type == BasicStates.starting:
        if message.text == "Admin" or message.text == "Client":
            await state.update_data({"User": message.text})
            await message.answer(text = "Registration or authorization?", reply_markup = registration_or_authorization_keyboard)
            await state.set_state(BasicStates.reg_or_auto)
        
    elif state_type == BasicStates.reg_or_auto:
        if message.text == "Registration" or message.text == "authorization":
            await state.update_data({"Enter type": message.text})
            if message.text == "Registration":
                await message.answer(text = "Enter your E-Mail (or 'Skip' if you don't want to): ", reply_markup = delete_keyboard)
                await state.set_state(BasicStates.registration)
            else:
                await message.answer(text = "Enter your LogIn: ", reply_markup = delete_keyboard)
                await state.set_state(BasicStates.authorization)

    elif state_type == BasicStates.authorization:
        data = await state.get_data()
        if "LogIn" in list(data):
            if "Password" in list(data):
                print("you arleady autorized")
            else:
                print("Login successfull")
                login_data = edit_database(command = f"SELECT login FROM {data['User']}_table")
                password_data = edit_database(command = f"SELECT password FROM {data['User']}_table")
                for value_num in range(len(login_data)):
                    login_data[value_num] = login_data[value_num][0]
                    password_data[value_num] = password_data[value_num][0]
                print(login_data)
                if data["LogIn"] in login_data:
                    if password_data[login_data.index(data["LogIn"])] == message.text:
                        print("Autorization successfull")
                        database_data = edit_database(command = f"SELECT * FROM {data['User'].lower()}_table")[login_data.index(data["LogIn"])]
                        if "Not_verified" in database_data[4]:
                            add_text = "You are still not verified as administrator."
                        elif "Verified" in database_data[4]:
                            admin_data = database_data[4].split(",")
                            add_text = f"Congarts! You are now administrator!\nThat means, that you have access to all functional which bot have.\nAlso, now you have contacts with other administrators and Owner.\nYou was verified by {admin_data[1]}"
                            edit_database(f"UPDATE {data['User'].lower()}_table SET info = 'True' WHERE login = '{data['LogIn']}'")
                        elif "True" in database_data[4]:
                            add_text = f"Welcome back, administrator {message.from_user.first_name}."
                        else:
                            add_text = ""
                        await message.answer(text = f"authorization successfull!\n{add_text}")
                        await state.update_data({"Password": message.text})
                        await state.update_data({"EMail": database_data[2]})
                        await state.update_data({"Phone_Number": database_data[3]})
                        await state.set_state(BasicStates.awaiting)
                    else:
                        await message.answer(text = "Password incorrect")
                        del data["LogIn"]
                        await state.set_data(data)
                else:
                    await message.answer(text = f"This login is invalid\nLog: {data['LogIn']}/{login_data}")
                    del data["LogIn"]
                    await state.set_data(data)
        else:
            await message.answer(text = "Enter password: ")
            await state.update_data({"LogIn": message.text})

    elif state_type == BasicStates.registration:
        data = await state.get_data()
        data_keys = list(data)
        if "EMail" in data_keys:
            if "Phone_Number" in data_keys:
                if "LogIn" in data_keys:
                    if "Password" in data_keys:
                        print("You are arleady registred")
                    else:
                        command = f"INSERT INTO {data['User'].lower()}_table (login, password, email, phone_number, info) VALUES ('{data['LogIn']}', '{message.text}', '{data['EMail']}', {data['Phone_Number']}, 'Not_verified')"
                        print(command)
                        edit_database(command)
                        if data["User"] == "Admin":
                            add_text = "\nBut, that doesn't means that you arleady have all functional which administrators have.\nYou need to wait for your verify by administrators to have all functional.\nWe will message you when this will happen.\nSee you later!"
                        else:
                            add_text = None
                        await message.answer(text = f"Registration successfull!{add_text}")
                        await state.update_data({"Password": message.text})
                        await state.set_state(BasicStates.awaiting)
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
        
        
    
# @dp.message(authorizationState())

# async def authorization(message)
    
async def run():
    await dp.start_polling(bot)

# asyncio.run(run())

