import os
import logging
import aiogram 
import aiogram.types as types
import aiogram.exceptions as exceptions
from aiogram.fsm import context
from .message import send_message
from modules.data_work import edit_database, find_path
from modules.keyboards import edit_message_keyboard, time_keyboard, list_names, list_time
from modules.all_states import AdminStates, SendStates
import modules.new_message as new_message
from modules.send_tools_message import send_admin_tools_message
import datetime
import time
import asyncio

funcs = []

def add_func(new_function):
    global funcs
    funcs.append(new_function)

async def send_edit_message(message: types.Message, state: context.FSMContext, bot: aiogram.Bot):
    if await state.get_state() == AdminStates.send_new_message:
        data = await state.get_data()
        try:
            await new_message.delete_messages(chat_id = message.chat.id, message_id = data["Edit_Message_ID"], bot = bot, state = state)
        except:
            print("no previous message")
        msg = await new_message.answer(message = message, text = "What do you want to do with this message?", reply_markup = edit_message_keyboard, reply_to_message_id = data['Message_ID'], bot = bot, state = state)
        data["Edit_Message_ID"] = msg.message_id
        await state.set_data(data = data)

def process_text(text: str | list, new_text_index: int):
    # print(text)
    # if isinstance(text, list):
    #     text = '&'.join(text)
    print(text)
    text[new_text_index] = text[new_text_index].replace("'", "`")
    print(text)
    text[new_text_index] = text[new_text_index].replace("&", " and ")
    print(text)
    if len(text[new_text_index]) > 900:
        text[new_text_index] = text[new_text_index][:900]
    return "&".join(text)
    
async def edit_message_handler(message: types.Message, state: context.FSMContext, bot: aiogram.Bot, dp = aiogram.Dispatcher):
    try:
        stat = await state.get_state()
        user_data = await state.get_data()
        data_db = edit_database(command = f"SELECT message FROM admin_table WHERE login = '{user_data['LogIn']}'")[0][0].split('&')
        if stat == SendStates.image:
            if message.photo != None:
                try:
                    if data_db[2] != "burger.png":
                        os.remove(find_path(f'message_images/{data_db[2]}'))
                except:
                    print('no image')
                name = f'{user_data["LogIn"]}.png'
                data_db[2] = name
                # print(f"UPDATE admin_table SET message = '{','.join(data_db)}' WHERE login = '{user_data['LogIn']}'")
                # print(message.photo[-1].height, message.photo)
                edit_database(f"UPDATE admin_table SET message = '{'&'.join(data_db)}' WHERE login = '{user_data['LogIn']}'")
                await bot.download(message.photo[-1], find_path(f"message_images/{name}"))
                print(user_data)
                print("s")
                await new_message.delete_messages(chat_id = message.chat.id, messages_id = user_data["Chat_History"][user_data["Chat_History"].index(user_data["Edit_Message_ID"]):], bot = bot, state = state)
                print("u")
                await bot.edit_message_media(media = types.InputMediaPhoto(media = types.FSInputFile(path = find_path(f"message_images/{name}")), caption = data_db[1]), chat_id = message.chat.id, message_id = user_data["Message_ID"])
                print("cc")
                await state.set_state(AdminStates.send_new_message)
                print("e")
                await send_edit_message(message = message, state = state, bot = bot)
                print("ss")
            else:
                print(message.text)
        elif stat == SendStates.description:
            data_db[1] = message.text
            data_db = process_text(data_db, 1)
            edit_database(fr"UPDATE admin_table SET message = '{data_db}' WHERE login = '{user_data['LogIn']}'")
            print(find_path(f"messages_images/burger.png"))
            print('b')
            data_db = data_db.split("&")
            await state.set_state(AdminStates.send_new_message)
            await new_message.delete_messages(chat_id = message.chat.id, messages_id = user_data["Chat_History"][user_data["Chat_History"].index(user_data["Edit_Message_ID"]):], bot = bot, state = state)
            await send_edit_message(message = message, state = state, bot = bot)
            await bot.edit_message_media(media = types.InputMediaPhoto(media = types.FSInputFile(path = find_path(f"message_images/{data_db[2]}")), caption = data_db[1]), chat_id = message.chat.id, message_id = user_data["Message_ID"])
        elif stat == SendStates.product:
            data_db[0] = message.text
            data_db = process_text(data_db, 0)
            edit_database(f'UPDATE admin_table SET message = "{data_db}" WHERE login = "{user_data["LogIn"]}"')
            await new_message.delete_messages(chat_id = message.chat.id, messages_id = user_data["Chat_History"][user_data["Chat_History"].index(user_data["Edit_Message_ID"]):], bot = bot, state = state)
            await state.set_state(AdminStates.send_new_message)
            await send_edit_message(message = message, state = state, bot = bot)
    except Exception as error:
        print(f"State: {state}")
        logging.error(f"No message: \n{error}")
    # pass

async def callback_edit_message_handler(callback: types.CallbackQuery, state: context.FSMContext, bot: aiogram.Bot, dp: aiogram.Dispatcher):
    text = callback.data.lower()
    data = await state.get_data()
    change = False
    if text == "edit_message_photo":
        stat = SendStates.image
        msg_text = "Send a new message photo: "
        change = True

    elif text == "edit_message_description":
        stat = SendStates.description
        msg_text = "Send a new message description: "
        change = True

    elif text == "edit_message_product":
        stat = SendStates.product
        msg_text = "Send a new message product name: "
        change = True

    elif text == "delay_message_sending":
        db = edit_database(command = f"SELECT message FROM admin_table WHERE login = '{data['LogIn']}'")[0][0]
        message = db.split("&")
        if len(message) > 3:
            message_time = message[3]
        else:
            message_time = datetime.datetime.today().strftime("%d.%m.%Y_%H:%M:%S")
            message = "&".join(message)
            edit_database(command = f"UPDATE admin_table SET message = '{'&'.join([message, message_time])}' WHERE login = '{data['LogIn']}'")
        message_second = datetime.datetime.strptime(message_time, r"%d.%m.%Y_%H:%M:%S").timestamp() - 1
        if message_second < time.time():
            time_text = "now"
        else:
            time_text = datetime.datetime.strptime(message_time, "%d.%m.%Y_%H:%M:%S").strftime("%d.%m.%Y %H:%M:%S")
        message = await new_message.answer(text = f"Your messages will be sent {time_text}", message = callback.message, state = state, reply_markup = time_keyboard, bot = bot, reply_to_message_id = data["Message_ID"])
        try:
            await new_message.delete_messages(messages_id = [data["Edit_Message_ID"]], chat_id = callback.message.chat.id, state = state, bot = bot)
        except Exception as error:
            print(f"Error while deleting message \n more information {error}")
        data["Edit_Message_ID"] = message.message_id
        await state.set_data(data = data)
        await state.set_state(state = SendStates.time)

    elif text == "send_message_to_groups":
        waited = False
        database_info = None
        time_delay = edit_database(command = f"SELECT message FROM admin_table WHERE login = '{data['LogIn']}'")[0][0].split("&")
        if len(time_delay)  >= 3:
            time_processed = datetime.datetime.strptime(time_delay[3], "%d.%m.%Y_%H:%M:%S")
            if time_processed.timestamp() > time.time():
                waited = True
                state = data.copy()
                database_info = edit_database(command = f"SELECT message FROM admin_table WHERE login = '{data['LogIn']}'")[0][0]
                database_info = database_info.split("&")
                await callback.answer(text = f"Your messages will be sent {time_processed.strftime('%d.%m.%Y %H:%M:%S')}")
                await asyncio.sleep(time_processed.timestamp() - time.time())
        successful = await send_message(message = callback, state = state, bot = bot, database_info = database_info)
        if not waited:
            print(successful)
            if isinstance(successful, list):
                if successful[1] >= 60:
                    text = f"{round(successful[1] // 60)} minutes and {round(successful[1] % 60)} seconds"
                else:
                    text = f"{round(successful[1] % 60)} seconds"   
                print("Good")
                await callback.answer(f"You are sending too often messages.\nPlease try again {text}")
            
            else:
                print("Bad")
                await callback.answer("Messages were sent!")
                await state.set_state(AdminStates.admin_awaiting)
                await new_message.delete_messages(chat_id = callback.message.chat.id, messages_id = [data["Message_ID"], data["Edit_Message_ID"]], bot = bot, state = state)
                await send_admin_tools_message(message = callback, state = state, user_id = callback.from_user.id)
                del data['Message_ID']
                del data["Edit_Message_ID"]
                await state.set_data(data = data)

    elif text == "cancel_edit_message":
        await state.set_state(AdminStates.admin_awaiting)
        print(data["Message_ID"], data["Edit_Message_ID"])
        await new_message.delete_messages(chat_id = callback.message.chat.id, messages_id = [data["Message_ID"], data["Edit_Message_ID"]], bot = bot, state = state)
        await send_admin_tools_message(message = callback, state = state, user_id = callback.from_user.id)
        del data["Admin_Tools_ID"]
        del data['Message_ID']
        del data['Edit_Message_ID']
        await state.set_data(data = data)
        await funcs[0]
        del funcs[0]

    if change:
        try:
            await new_message.delete_messages(chat_id = callback.message.chat.id, messages_id = [callback.message.message_id], bot = bot, state = state)
        except exceptions.TelegramBadRequest as error:
            print("there is no message")
        except Exception as error:
            print(f"Some error occured.\n{error}")
        await state.set_state(stat)
        if "Message_ID" not in list(data):
            await send_message(message = callback.message, state = state, bot = bot, test = 1)
        new_id = await new_message.answer(message = callback.message, text = msg_text, reply_to_message_id = data["Message_ID"], bot = bot, state = state)
        data["Edit_Message_ID"] = new_id.message_id
        await state.set_data(data = data)
        
async def delay_callbac_handler(callback: types.CallbackQuery, state: context.FSMContext, bot = aiogram.Bot):
    if await state.get_state() == SendStates.time:
        print("Good")
        data = await state.get_data()
        counter = 0
        finded = False
        if "close_time_message" in callback.data.lower():
            await new_message.delete_messages(messages_id = [callback.message.message_id], chat_id = callback.message.chat.id, state = state, bot = bot)
            await state.set_state(AdminStates.send_new_message)
            await send_edit_message(message = callback.message, state = state, bot = bot)
            return 0 
        try:
            while counter < len(list(list_names)) - 2 or not finded:
                print(counter)
                if list(list_names)[counter] in callback.data:
                    print("Found!")
                    message = edit_database(command = f"SELECT message FROM admin_table WHERE login = '{data['LogIn']}'")[0][0]
                    message = message.split("&")
                    message_time = datetime.datetime.strptime(message[3], "%d.%m.%Y_%H:%M:%S")
                    callback_data = callback.data.split("_")
                    if callback_data[1] != callback_data[0]:
                        message_seconds = round(message_time.timestamp())
                        message_seconds += int(callback_data[1]) * list_names[callback_data[0]]
                        if message_seconds <= time.time():
                            print(message_seconds, time.time())
                            text = "now"
                            message_seconds = time.time()
                        else:
                            text = datetime.datetime.fromtimestamp(message_seconds).strftime('%d.%m.%Y %H:%M:%S')
                        try:
                            await callback.message.edit_text(text = f"Your message will be sent {text}", 
                                                            inline_message_id = str(callback.message.message_id), reply_markup = callback.message.reply_markup)
                        except:
                            print("There is an error.\nI don't know why.\n")
                        del message[3]
                        message = "&".join(message)
                        edit_database(f"UPDATE admin_table SET message = '{'&'.join([message, datetime.datetime.fromtimestamp(message_seconds).strftime('%d.%m.%Y_%H:%M:%S')])}' WHERE login = '{data['LogIn']}'")
                    else:
                        await callback.answer(f"Yes, it's a {callback_data[0]}.")
                    finded = 1
                    return 
                counter += 1
        except:
            print("\nSomething went REALLY wrong...\n")

        