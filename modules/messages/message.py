import time
import aiogram 
import aiogram.types as types
from aiogram.fsm import context
from modules.data_work import edit_database, find_path


async def send_message(message: types.Message | types.CallbackQuery, state: context.FSMContext | dict, bot: aiogram.Bot, test: bool = False, database_info: list = None):
    if isinstance(state, context.FSMContext):
        data = await state.get_data()
    else:
        data = state
    user_data = [message.from_user.first_name, message.from_user.last_name]
    if isinstance(message, types.CallbackQuery):
        message = message.message
    if database_info == None:
        message_info = edit_database(command = f"SELECT message FROM admin_table WHERE login = '{data['LogIn']}'")[0][0]
        print(f"Raw: {message_info}")
        message_info = message_info.split("&")
        print(f"Cooked: {message_info}")
    else:
        message_info = database_info
    image = aiogram.types.FSInputFile(find_path(f"message_images/{message_info[2]}"))
    time_ = edit_database(command = f"SELECT message_cd FROM admin_table WHERE login = '{data['LogIn']}'")[0][0]
    if time_ != None:
        time_ = int(time_)
    else:
        time_ = 0
    description = f"{message_info[1]}\n\nFrom {user_data[0]} {user_data[1]}"
    name_product = message_info[0]
    print(1)
    if test:
        name_product = "admin"
    buy_button = types.InlineKeyboardButton(text = "BUY", callback_data = f"buy?{name_product}?0")
    reject_button = types.InlineKeyboardButton(text = "REJECT", callback_data = f"reject?{name_product}")
    # accept_button = types.InlineKeyboardButton(text = "ACCEPT", callback_data = f"accept_{name_product}")
    message_inline_keyboard = types.InlineKeyboardMarkup(inline_keyboard = [[buy_button, reject_button]])
    print(2)
    if test:
        print(3)
        msg = await message.answer_photo(photo = image, caption = description)
        data['Message_ID'] = msg.message_id
        await state.set_data(data = data)
        print(4)
    elif time.time() >= time_ + 900:
        group = edit_database(command = f"SELECT * FROM data")[0][0].split(",")
        edit_database(command = f"UPDATE admin_table SET message_cd = {round(time.time())} WHERE login = '{data['LogIn']}'") 
        for id in group:
            try:
                msg = await bot.send_photo(chat_id = id, photo = image, caption = description, reply_markup = message_inline_keyboard)
                print("send")
            except:
                print(id)
    else:
        return [False, time_ + 900 - time.time()]


async def processing_callbacks_group_messages(callback: types.CallbackQuery, state: context.FSMContext):
    data = await state.get_data()
    # print(data)
    if "admin" not in callback.data and await state.get_state() == None:
        if "buy" in callback.data:
            print(callback.from_user.first_name)
            count = int(callback.data.split('?')[-1]) + 1
            name_product = callback.data.split('?')[1]
            if name_product in list(data):
                user_count = data[name_product]
            else:
                user_count = 0
            data[name_product] = user_count + 1
            if count == 1 :
                accept_button = types.InlineKeyboardButton(text = "ACCEPT", callback_data = f"accept?{name_product}")
                callback.message.reply_markup.inline_keyboard.append([accept_button])
            callback.message.reply_markup.inline_keyboard[0][0].text = f"Buy overall {count}"
            callback.message.reply_markup.inline_keyboard[0][0].callback_data = f"buy?{name_product}?{count}"
            await callback.answer(text = f"You choosed {data[name_product]} {name_product}s")
            await callback.message.edit_reply_markup(inline_message_id = callback.inline_message_id, reply_markup = callback.message.reply_markup)
            await state.set_data(data = data)
        elif "reject" in callback.data:
            info = callback.message.reply_markup.inline_keyboard[0][0].callback_data.split('?')
            name_product = callback.data.split("?")[1]
            count = int(info[-1]) - 1
            if name_product in data:
                user_count = data[name_product] - 1
                if user_count >= 0 and count >= 0:
                    data[name_product] -= 1
                    if count == 0:
                        del callback.message.reply_markup.inline_keyboard[1][0]
                        callback.message.reply_markup.inline_keyboard[0][0].text = "Buy first"
                    else:
                        callback.message.reply_markup.inline_keyboard[0][0].text = f"Buy overall {count}"
                    callback.message.reply_markup.inline_keyboard[0][0].callback_data = f"buy?{info[1]}?{count}"
                    name_product = info[1]
                    await state.set_data(data = data)
                    await callback.message.edit_reply_markup(inline_message_id = callback.inline_message_id, reply_markup = callback.message.reply_markup)
                else:
                    text_head = "Buy any number of this product to reject your purchase of this product."
                    text_tail = "(pretty logical)"
                    space_count = len(text_head) - len(text_tail)
                    await callback.answer(text = f"{text_head}\n{' ' * space_count}{text_tail}")
            else:
                text_head = "Buy any number of this product to reject your purchase of this product."
                text_tail = "(pretty logical)"
                space_count = len(text_head) - len(text_tail)
                await callback.answer(text = f"{text_head}\n{' ' * space_count}{text_tail}")

        elif "accept" in callback.data:
            message_info = callback.message.reply_markup.inline_keyboard[0][0].callback_data.split('?')
            print(message_info, data)
            if message_info[1] in list(data):
                if data[message_info[1]] > 0:
                    # print(data, 3)
                    database = edit_database(f"SELECT * FROM products")
                    usernames = []
                    for user in database:
                        usernames.append(user[0])
                    product = message_info[1]
                    text = f"{product}:{data[message_info[1]]}"
                    print(text, usernames, 2)
                    if callback.from_user.username in usernames:
                        for data_db in database:
                            if data_db[0] == callback.from_user.username:
                                database = database[database.index(data_db)]
                                break
                        print(database, 5)
                        products = database[1].split(",")
                        product_names = []
                        for product_ in products:
                            product_names.append(product_.split(":")[0])
                        if product in product_names:
                            products[product_names.index(product)] = text
                        else:
                            products.append(text)
                        print(product_names, products, 1)
                        data_ = ",".join(products)
                        print(data, data_)
                        edit_database(f"UPDATE products SET products = '{data_}' WHERE username = '{callback.from_user.username}'") 
                    else:
                        edit_database(f"INSERT INTO products (username, products) VALUES ('{callback.from_user.first_name}', '{text}')")
                    count = int(message_info[2]) - data[message_info[1]]
                    del data[message_info[1]]
                    await state.set_data(data)
                    callback.message.reply_markup.inline_keyboard[0][0].text = f"Buy overall {count}"
                    callback.message.reply_markup.inline_keyboard[0][0].callback_data = f"buy?{message_info[1]}?{count}"
                    if count < 1:
                        callback.message.reply_markup.inline_keyboard[0][0].text = f"Buy first"
                        del callback.message.reply_markup.inline_keyboard[1][0]
                        callback.message.reply_markup.inline_keyboard[0][0].callback_data = f"buy?{message_info[1]}?0"
                    await callback.message.edit_reply_markup(inline_message_id = callback.inline_message_id, reply_markup = callback.message.reply_markup)
                else:
                    await callback.answer("You don't purchased this product!")
                    print(message_info[1], data, 4)
            else:
                await callback.answer("You don't purchased this product!")
                print(message_info[1], data, 4)
