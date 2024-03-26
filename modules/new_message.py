import aiogram
import aiogram.types as types
from aiogram.fsm import context
from aiogram.fsm.storage.base import StorageKey

async def answer(message: types.Message, text: str, reply_markup = None, state: context.FSMContext = None, reply_to_message_id: int = None, bot: aiogram.Bot = None):
    if reply_to_message_id == None:
        msg = await message.answer(text = text, reply_markup = reply_markup)
    else:
        if bot == None:
            print("Add bot parameter")
        else:
            msg = await bot.send_message(chat_id = message.chat.id, text = text, reply_to_message_id = reply_to_message_id, reply_markup = reply_markup)
    data = await state.get_data()
    if "Chat_History" in list(data):
        data["Chat_History"].append(msg.message_id)
    else:
        data["Chat_History"] = [msg.message_id]
    await state.set_data(data)
    return msg

async def delete_messages(messages_id: list, chat_id: int, state: context.FSMContext, bot: aiogram.Bot):
    data = await state.get_data()
    for message_id in messages_id:
        try:
            await bot.delete_message(chat_id = chat_id, message_id = message_id)
            data["Chat_History"].remove(message_id)
        except Exception as error:
            print(f"{message_id}\n{error}")
    await state.set_data(data)

async def send_message(chat_id: int, text: str, bot: aiogram.Bot, dp: aiogram.Dispatcher, reply_markup = None):
    state = context.FSMContext(
        storage = dp.storage,
        key = StorageKey(bot_id = bot.id, chat_id = chat_id, user_id = chat_id)
    )
    message = await bot.send_message(chat_id, text, reply_markup = reply_markup)
    data = await state.get_data()
    data["Chat_History"].append(message.message_id)
    print(f"Add new: {data}")
    await state.set_data(data)
        
async def clean_chat_history(state: context.FSMContext, bot: aiogram.Bot, chat_id: int):
    data = await state.get_data()
    print(f"Clean all: {data}")
    history = data["Chat_History"]
    try:
        history.append(data["Edit_Message_ID"])
        del data["Edit_Message_ID"]
    except:
        print("No edit")
    for message_id in history:
        try:
            await bot.delete_message(chat_id, message_id)
        except Exception as error:
            print(error)
    data["Chat_History"] = []
    await state.set_data(data)
    return state

async def add_id(state: context.FSMContext, message_id: int):
    data = await state.get_data()
    print("????????????????????")
    if "Chat_History" in list(data):
        data["Chat_History"].append(message_id)
    else: 
        data["Chat_History"] = [message_id]
    await state.set_data(data) 