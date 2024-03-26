import aiogram
import aiogram.types as types
import aiogram.fsm.context as context
from modules.data_work import edit_database
from modules.all_states import BasicStates, AdminStates
import modules.new_message as new_message

async def authorization_(message: types.Message, state: context.FSMContext, bot: aiogram.Bot):
    data = await state.get_data()
    if "LogIn" in list(data):
        if "Password" in list(data):
            print("you arleady autorized")
            print(await state.get_state())
        else:
            print("Login successfull")
            login_data = edit_database(command = f"SELECT login FROM {data['User']}_table")
            password_data = edit_database(command = f"SELECT password FROM {data['User']}_table")
            chat_id_data = edit_database(command = f"SELECT chat_id FROM {data['User']}_table") 
            for value_num in range(len(login_data)):
                login_data[value_num] = login_data[value_num][0]
                password_data[value_num] = password_data[value_num][0]
            print(login_data)
            if data["LogIn"] in login_data:
                index_key = login_data.index(data["LogIn"])
                if password_data[index_key] == message.text:
                    print(chat_id_data, index_key)
                    if chat_id_data[index_key][0] == 0:
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
                            edit_database(command = f"UPDATE admin_table SET message = 'burgero&It`s a burger!&burger.png' WHERE login = '{data['LogIn']}'")
                            edit_database(f"UPDATE {data['User'].lower()}_table SET info = 'True' WHERE login = '{data['LogIn']}'")
                        elif "True" in database_data[4]:
                            new_state = AdminStates.admin_awaiting
                            add_text = f"Welcome back, administrator {message.from_user.first_name}.\nFor administration use /tools. For watching your profile use."
                        elif "Rejected" in database_data[4]:
                            add_text = "Your application for administrator was rejected. This account will be deleted.\nWe are sorry for this."
                            edit_database(f"DELETE FROM admin_table WHERE login = '{data['LogIn']}'")
                        else:
                            add_text = ""

                        data.update({"Password": message.text, "EMail": database_data[2], "Phone_Number": database_data[3], "Past_State": new_state, "Past_Message": ["You are authorized", None]})
                        data["Past_Data"] = data
                        await state.set_data(data = data)
                        await new_message.clean_chat_history(state, bot, message.chat.id)
                        await new_message.answer(text = f"Authorization successfull! If you want to leave your account use /leave. \nFor watching your profile use /profile. \n{add_text}", message = message, state = state)
                        await state.set_state(new_state)
                    else:
                        await new_message.answer(text = "This account is already in use", message = message, state = state)
                        del data["LogIn"]
                        await state.set_data(data)
                else:
                    await new_message.answer(text = "Password incorrect.\nEnter your password: ", message = message, state = state)
            else:
                await new_message.answer(text = f"This login is invalid.\nEnter your login: ", message = message, state = state)
                del data["LogIn"]
                await state.set_data(data)
    else:
        await new_message.answer(text = "Enter password: ", message = message, state = state)
        await state.update_data({"LogIn": message.text})
