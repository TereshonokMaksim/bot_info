import aiogram
import aiogram.types as types
import aiogram.filters as filters
import aiogram.methods as methods
from aiogram.fsm import context, state
from aiogram.fsm.storage.base import StorageKey
from modules.all_states import BasicStates
from modules.keyboards import admin_or_client_keyboard
from modules.data_work import edit_database
import modules.new_message as new_message

async def leave_account(message: types.Message, state: context.FSMContext, bot: aiogram.Bot):
    if await state.get_state() not in (BasicStates.authorization, BasicStates.registration, BasicStates.none_state, BasicStates.starting, BasicStates.reg_or_auto):
        try:
            await new_message.clean_chat_history(state, bot, message.chat.id)
            data = await state.get_data()
            # edit_database(f"UPDATE {data['User']}_table SET user_id = 0 WHERE login = '{data['LogIn']}'")
            edit_database(f"UPDATE {data['User']}_table SET chat_id = 0 WHERE login = '{data['LogIn']}'")
            await state.set_data({})
            await new_message.answer(text = "You leaved your account", message = message, state = state)
            await new_message.answer(text = "Hi, user! Choose admin or client", reply_markup = admin_or_client_keyboard, message = message, state = state) 
            data = await state.get_data()
            data["Past_State"] = BasicStates.starting
            data["Past_Message"] = ["Hi, user! Choose admin or client", admin_or_client_keyboard]
            data["Past_Data"] = data
            await state.set_data(data)
            await state.set_state(BasicStates.starting)
        except:
            await new_message.answer(message = message, text = "You can't leave account while you not in account.", state = state)

async def kick_from_account(chat_id: int, dp: aiogram.Dispatcher = None, bot: aiogram.Bot = None, user_id: int = None):
    message = await bot.send_message(chat_id = chat_id, text = "You was kicked out of your account.\nFor create or enter in new account use /start.")
    state = context.FSMContext(
        storage = dp.storage,
        key = StorageKey(bot_id = bot.id, chat_id = chat_id, user_id = user_id)
    )
    if await state.get_state() not in (BasicStates.authorization, BasicStates.registration, BasicStates.none_state, BasicStates.starting, BasicStates.reg_or_auto):
        try:
            data = await state.get_data()
            edit_database(command = f"UPDATE {data['User']}_table SET chat_id = 0 WHERE login = {data['LogIn']}")
            # edit_database(command = f"UPDATE {data['User']}_table SET user_id = 0 WHERE login = {data['LogIn']}")
            data = {}
            data["Past_State"] = BasicStates.starting
            data["Past_Message"] = ["Hi, user! Choose admin or client", admin_or_client_keyboard]
            data["Past_Data"] = data
            await new_message.clean_chat_history(state, bot, chat_id)
            await state.set_state(BasicStates.starting)
            await state.set_data(data = data)
        except:
            await new_message.answer(message = message, text = "We was about to kick you from your account, but congarts, we can't.")