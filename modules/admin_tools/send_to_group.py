import aiogram
from aiogram import types
from aiogram.fsm import context
from aiogram.fsm.storage.base import StorageKey
from modules.data_work import edit_database
from modules.all_states import AdminStates, BasicStates
from modules.keyboards import verif_user_keyboard, admin_keyboard
from .main import send_verif_page_message

async def make_an_annoucment(message: types.Message, state: context.FSMContext, bot: aiogram.Bot):
    if await state.get_state() == AdminStates.send_new_message:
        data = await state.get_data()
        data_keys = list(data)
        if "SM_Theme" in data_keys:
            if "SM_Content" in data_keys:
                if "SM_Floor" in data_keys:
                    await state.set_state(AdminStates.admin_awaiting)
                    if message.text.lower() in ["y", "ye", "yes", "es", "yep", "true", "1", "good", "great", "send"]:
                        group_ids = edit_database(command = "SELECT * FROM data WHERE seeker = 1")[0][0]
                        print(group_ids)
                        group_ids = group_ids.split(",")
                        # del group_ids[0]
                        for id in group_ids:
                            try:
                                await bot.send_message(chat_id = id, text = (f"{data['SM_Theme']}\n\n{data['SM_Content']}\n\n{data['SM_Floor']}"))
                                print("send")
                            except:
                                print(id)
                        await message.answer("Messages were sent!")
                    else:
                        await message.answer("Message cancelled")
                    del data['SM_Theme']
                    del data['SM_Content']
                    del data['SM_Floor']
                    await state.set_data(data = data)
                    await message.answer(text = "To use admin tools again just use /tools.")
                else:
                    await message.answer("Great! Now, i send to you entire message and you approve it with messages 'Yes' or 'No'.")
                    await message.answer(f"{data['SM_Theme']}\n\n{data['SM_Content']}\n\n{message.text}")
                    await state.update_data({"SM_Floor": message.text})
            else:
                await message.answer("Good, now, send only the end of message.")
                await state.update_data({"SM_Content": message.text})
        else:
            await message.answer("Okay, send entire message (without title and end (end part means part of the message, where is write something like 'By Tom')).")
            await state.update_data({"SM_Theme": message.text})
            