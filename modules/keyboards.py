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

verif_page_keyboard = types.InlineKeyboardMarkup(inline_keyboard = [[types.InlineKeyboardButton(text = "Reject all", callback_data = "reject_all")],
    [types.InlineKeyboardButton(text = "Close", callback_data = "close_verif_page")]]) 

verif_user_keyboard = types.InlineKeyboardMarkup(inline_keyboard = [[types.InlineKeyboardButton(text = "Accept", callback_data = "verif_accept")],
                                                                    [types.InlineKeyboardButton(text = "Reject", callback_data = "verif_reject")],
                                                                    [types.InlineKeyboardButton(text = "Close", callback_data = "close_verif")]])

delete_keyboard = types.ReplyKeyboardRemove()