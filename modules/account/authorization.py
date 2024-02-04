import aiogram.types as types
import aiogram.fsm.context as context
from modules.data_work import edit_database
from modules.all_states import BasicStates, AdminStates

async def authorization_(message: types.Message, state: context.FSMContext):
    data = await state.get_data()
    if "LogIn" in list(data):
        if "Password" in list(data):
            print("you arleady autorized")
            print(await state.get_state())
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
                    edit_database(f"UPDATE {data['User']}_table SET user_id = {message.from_user.id} WHERE login = '{data['LogIn']}'")
                    edit_database(f"UPDATE {data['User']}_table SET chat_id = {message.chat.id} WHERE login = '{data['LogIn']}'")
                    new_state = BasicStates.awaiting
                    if "Not_verified" in database_data[4]:
                        add_text = "You are still not verified as administrator."
                    elif "Verified" in database_data[4]:
                        admin_data = database_data[4].split(",")
                        new_state = AdminStates.admin_awaiting
                        add_text = f"Congarts! You are now administrator!\nThat means, that you have access to all functional which bot have.\nYou was verified by {admin_data[1]}. To start using admin tools use /tools."
                        edit_database(f"UPDATE {data['User'].lower()}_table SET info = 'True' WHERE login = '{data['LogIn']}'")
                    elif "True" in database_data[4]:
                        new_state = AdminStates.admin_awaiting
                        add_text = f"Welcome back, administrator {message.from_user.first_name}.\nFor administration use /tools."
                    elif "Rejected" in database_data[4]:
                        add_text = "Your application for administrator was rejected. This account will be deleted.\nWe are sorry for this."
                        edit_database(f"DELETE FROM admin_table WHERE login = '{login_data.index(data['LogIn'])}'")
                    else:
                        add_text = ""
                    await message.answer(text = f"Authorization successfull! If you want to leave your account use /leave.\n{add_text}")
                    await state.update_data({"Password": message.text})
                    await state.update_data({"EMail": database_data[2]})
                    await state.update_data({"Phone_Number": database_data[3]})
                    await state.set_state(new_state)
                else:
                    await message.answer(text = "Password incorrect.\nEnter your password: ")
            else:
                await message.answer(text = f"This login is invalid.\nEnter your login: ")
                del data["LogIn"]
                await state.set_data(data)
    else:
        await message.answer(text = "Enter password: ")
        await state.update_data({"LogIn": message.text})