import aiogram
from aiogram import types
from aiogram.fsm import context
from aiogram.fsm.storage.base import StorageKey
from modules.data_work import edit_database
from modules.all_states import AdminStates, BasicStates
from modules.keyboards import verif_user_keyboard, admin_keyboard
from modules.account.leave_acc import kick_from_account
from .main import send_verif_page_message

async def verification(message: types.Message, state: context.FSMContext):
    if await state.get_state() == AdminStates.verif_page:
        data = await state.get_data()
        data_keys = list(data)

        if "Verif_User" in data_keys:
            pass    
        else:
            data_database = edit_database("SELECT * FROM admin_table")
            print(data_database)
            text = message.text
            logins = []
            for user in data_database:
                if "Not_verified" in user[4]:
                    logins.append(user[0])
            try:
                id = int(text)
                if 0 < id <= len(logins):
                    user_login = logins[id - 1]
                else:
                    await message.answer("Wrong user number.\nCheck application list which was sent earlier.")
                    return 0
            except:
                if text in logins:
                    user_login = text
                else:
                    await message.answer("Wrong login.\nCheck application list which was sent earlier.")
                    return 0

            await state.update_data({"Verif_User": user_login})
            user_data = edit_database(f"SELECT * FROM admin_table WHERE login = '{user_login}'")[0]
            print(user_data)
            await message.answer(text = f"{user_login} information: \n\nEMail: {user_data[2]}; \nPhone number: {user_data[3]}. \n\nApplication: {user_data[5]} \n\nWould you like to accept this user to administration?", reply_markup = verif_user_keyboard)


async def close_application(state: context.FSMContext, callback: types.CallbackQuery, show: bool):
    print("Closing")
    try:
        data = await state.get_data()
        del data['Verif_User']
    except:
        print("Rejecting all")
    await state.set_data(data)
    if show:
        try:
            await callback.message.delete()
        except:
            print(":(")
        await send_verif_page_message(message = callback.message)


async def reject(callback: types.CallbackQuery, data: dict, dp: aiogram.Dispatcher, bot: aiogram.Bot, state: context.FSMContext, login: str, ver_page_show: bool):
    database_data = edit_database(f"SELECT * FROM admin_table WHERE login = '{login}'")[0]
    if database_data[6] != 0:
        await bot.send_message(chat_id = database_data[7],
                            text = "Your application for administrator was rejected. This account will be deleted.\nWe are sorry for this.")
        await kick_from_account(chat_id = database_data[7], dp = dp, bot = bot, user_id = database_data[6])
        edit_database(f"DELETE FROM admin_table WHERE login = '{login}'")
    else:
        edit_database(f"UPDATE admin_table SET info = 'Rejected' WHERE login = '{login}'")
    await close_application(state = state, callback = callback, show = ver_page_show)


async def verification_callbacks(callback: types.CallbackQuery, state: context.FSMContext, bot: aiogram.Bot, dp: aiogram.Dispatcher):
    data = await state.get_data()
    data_keys = list(data)
    print(f"Start: {await state.get_state()}")
    if await state.get_state() == AdminStates.verif_page:
        print(f"Continue: {data_keys}")
        if "Verif_User" in data_keys:
            print(f"Almost end: {callback.data}")
            if callback.data == "verif_accept":
                database_data = edit_database(f"SELECT * FROM admin_table WHERE login = '{data['Verif_User']}'")[0]
                await callback.message.answer(f"You verified {data['Verif_User']}. \nWe will message him.")
                print(database_data)
                if database_data[6] != 0:
                    await bot.send_message(
                                           chat_id = database_data[7], 
                                           text = f"Congarts! You are now administrator!\nThat means, that you have access to all functional which bot have.\nYou was verified by {data['LogIn']}. To start using admin tools use /tools."
                                           )
                    edit_database(f"UPDATE admin_table SET info = 'True' WHERE login = '{data['Verif_User']}'")
                    data_database = edit_database(f"SELECT * FROM admin_table WHERE login = '{data['Verif_User']}'")[0]
                    user_state = context.FSMContext(
                        storage = dp.storage,
                        key = StorageKey(bot_id = bot.id, chat_id = data_database[7], user_id = data_database[6])
                    )
                    await user_state.set_state(AdminStates.admin_awaiting)
                else:
                    edit_database(f"UPDATE admin_table SET info = 'Verified,{data['LogIn']}' WHERE login = '{data['Verif_User']}'")
                await close_application(state = state, callback = callback, show = True)

            elif callback.data == "verif_reject":
                await callback.message.answer(f"You rejected {data['Verif_User']} application. \nWe will message him.")
                await reject(callback = callback, data = data, dp = dp, bot = bot, state = state, login = data['Verif_User'], ver_page_show = True)

            elif callback.data == "close_verif":
                await close_application(state = state, callback = callback, show = True)
        else:
            if callback.data == "reject_all":
                data_database = edit_database("SELECT * FROM admin_table")
                print(data_database)
                for user in data_database:
                    if "Not_verified" in user[4]:
                        await reject(callback = callback, data = data, dp = dp, bot = bot, state = state, login = user[0], ver_page_show = False)
                await state.set_state(AdminStates.admin_awaiting)
                await callback.message.answer(f"You succefully reject all applications.")
                await callback.message.answer(text = f"Ok, what do you want to do now, {data['LogIn']}?", reply_markup = admin_keyboard)

            elif callback.data == "close_verif_page":
                try:
                    await callback.message.delete()
                    await callback.message.answer(text = f"Ok, what do you want to do now, {data['LogIn']}?", reply_markup = admin_keyboard)
                except:
                    print("verif page was opened more than 48 hours ago")
                await state.set_state(AdminStates.admin_awaiting)

