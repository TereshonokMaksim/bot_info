import aiogram
from aiogram import types
from aiogram.fsm import context 
from modules.messages import send_edit_message
from modules.all_states import AdminStates, SendStates
import modules.new_message as new_message


async def cancel(message: types.Message, state: context.FSMContext, bot: aiogram.Bot):
    data = await state.get_data()
    if await state.get_state() not in [AdminStates.send_new_message, SendStates.description, SendStates.edit, SendStates.image, SendStates.product, SendStates.time]:
        try:
            print(data["Chat_History"])
            await new_message.clean_chat_history(state, bot, message.chat.id)
            await state.set_state(state = data["Past_State"])
            await state.set_data(data = data["Past_Data"])
            await new_message.answer(text = data["Past_Message"][0], reply_markup = data["Past_Message"][1], message = message, state = state)
        except Exception as error:
            print(error, data)
            await new_message.answer("There is, probably, no other stage where you were, so you can do everything from start.")
            await state.set_state(None)
    else:
        try:
            await state.set_state(AdminStates.send_new_message)
            await new_message.delete_messages(chat_id = message.chat.id, messages_id = [data["Edit_Message_ID"]], bot = bot, state = state) 
            await message.delete()
            await send_edit_message(message = message, state = state, bot = bot)
        except Exception as error:
            await new_message.answer(text = f"There is unknown error.\nLog: {error}", message = message, state = state)