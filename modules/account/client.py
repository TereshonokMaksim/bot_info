import aiogram
from aiogram import types
from aiogram.fsm import context
from modules.all_states import BasicStates
from modules.keyboards import registration_or_authorization_keyboard, delete_keyboard

async def enter(message: types.Message, state: context.FSMContext):
    if message.text == "Admin" or message.text == "Client":
        await state.update_data({"User": message.text})
        await message.answer(text = "Registration or authorization?", reply_markup = registration_or_authorization_keyboard)
        await state.set_state(BasicStates.reg_or_auto)
    
async def author_or_reg(message: types.Message, state: context.FSMContext):
    if message.text == "Registration" or message.text == "Authorization":
        await state.update_data({"Enter type": message.text})
        if message.text == "Registration":
            await message.answer(text = "Enter your E-Mail (or 'Skip' if you don't want to): ", reply_markup = delete_keyboard)
            await state.set_state(BasicStates.registration)
        else:
            await message.answer(text = "Enter your LogIn: ", reply_markup = delete_keyboard)
            await state.set_state(BasicStates.authorization)