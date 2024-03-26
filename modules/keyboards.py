from aiogram import types

admin_button = types.KeyboardButton(text = "Admin")
client_button =  types.KeyboardButton(text = "Client")
admin_or_client_keyboard = types.ReplyKeyboardMarkup(keyboard = [[admin_button, client_button]])

reg_button = types.KeyboardButton(text = "Registration")
autoris_button = types.KeyboardButton(text = "Authorization")
registration_or_authorization_keyboard = types.ReplyKeyboardMarkup(keyboard = [[reg_button, autoris_button]])

open_verification_page = types.InlineKeyboardButton(text = "Open applications", callback_data = "verif_page")
open_send_page = types.InlineKeyboardButton(text = "Send new message", callback_data = "new_message")
admin_keyboard = types.InlineKeyboardMarkup(inline_keyboard = [[open_send_page], [open_verification_page]])
admin_uncomplete_keyboard = types.InlineKeyboardMarkup(inline_keyboard = [[open_send_page]])

verif_page_keyboard = types.InlineKeyboardMarkup(inline_keyboard = [[types.InlineKeyboardButton(text = "Reject all", callback_data = "reject_all")],
    [types.InlineKeyboardButton(text = "Close", callback_data = "close_verif_page")]]) 

verif_user_keyboard = types.InlineKeyboardMarkup(inline_keyboard = [[types.InlineKeyboardButton(text = "Accept", callback_data = "verif_accept")],
                                                                    [types.InlineKeyboardButton(text = "Reject", callback_data = "verif_reject")],
                                                                    [types.InlineKeyboardButton(text = "Close", callback_data = "close_verif")]])

photo_button = types.InlineKeyboardButton(text = "Change photo", callback_data = "edit_message_photo")
description_button = types.InlineKeyboardButton(text = "Change description", callback_data = "edit_message_description")
product_button = types.InlineKeyboardButton(text = "Change product", callback_data = "edit_message_product")
edit_message_time = types.InlineKeyboardButton(text = "Delay message", callback_data = "delay_message_sending")
send_message_button = types.InlineKeyboardButton(text = "Send message", callback_data = "send_message_to_groups")
close_message = types.InlineKeyboardButton(text = "Cancel sending message", callback_data = "cancel_edit_message")
edit_message_keyboard = types.InlineKeyboardMarkup(inline_keyboard = [[photo_button, description_button],
                                                                      [product_button, edit_message_time],
                                                                      [close_message, send_message_button]])

list_names = {"day": 86400, "hour": 3600, "minute": 60, "second": 1}
list_time = ["-5", "-1", "", "+1", "+5"]
list_time_buttons = []
for name_num in range(len(list(list_names))): 
    list_time_buttons.append([]) 
    list_time[round(len(list_time) / 2 - 1)] = list(list_names)[name_num] 
    for button_text in list_time: 
        list_time_buttons[name_num].append(types.InlineKeyboardButton(text = button_text, callback_data = f"{list(list_names)[name_num]}_{button_text}")) 

leave_button = types.InlineKeyboardButton(text = "Save", callback_data = "close_time_message")
list_time_buttons.append([leave_button])
time_keyboard = types.InlineKeyboardMarkup(inline_keyboard = list_time_buttons)

edit_profile = types.InlineKeyboardButton(text = "Edit profile", callback_data = "edit_prof")
leave_profile = types.InlineKeyboardButton(text = "Leave account", callback_data = "leave_acc")
close_profile = types.InlineKeyboardButton(text = "Close profile", callback_data = "close_prof")
profile_keyboard = types.InlineKeyboardMarkup(inline_keyboard = [[edit_profile], [leave_profile], [close_profile]])

button_names = {"Password": ["password", "Password"], "E Mail": ["email", "EMail"], "Phone Number": ["phone_number", "Phone_Number"], "Close": ["Hi!", "what are ya doing here?"]}
buttons = [types.InlineKeyboardButton(text = name, callback_data = f"change_{name.lower()}") for name in list(button_names)]
keyboard_changes = types.InlineKeyboardMarkup(inline_keyboard = [[buttons[0], buttons[1]], [buttons[2], buttons[3]]])

delete_keyboard = types.ReplyKeyboardRemove()