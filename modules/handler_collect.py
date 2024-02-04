#PARKING SUPER FREE NO SCAM!!! skachat brawl stars bez virusov besplatno pro max no registration and sms or mms
import modules.account as account
import modules.groups as groups
import modules.admin_tools as admin_tools
import aiogram
from aiogram import types
from aiogram.fsm import context
from modules.all_states import BasicStates, AdminStates

def launcher(dp: aiogram.Dispatcher, bot: aiogram.Bot):
    
    @dp.message()

    async def runner(message: types.Message, state: context.FSMContext):
        await admin_tools.application_checker(message = message, state = state)

        if await state.get_state() == BasicStates.starting:
            await account.enter(message = message, state = state)
            
        elif await state.get_state() == BasicStates.reg_or_auto:  
            await account.author_or_reg(message = message, state = state)  

        elif await state.get_state() == BasicStates.registration:
            await account.registration_(message = message, state = state)

        elif await state.get_state() == BasicStates.authorization:
            await account.authorization_(message = message, state = state)

        elif await state.get_state() == BasicStates.awaiting or await state.get_state() == AdminStates.admin_awaiting:
            if message.text.lower() == "/leave":
                await account.leave_account(message = message, state = state)

        else:
            try:
                if message.text.lower() == "/start":
                    await account.start(message = message, state = state)
            except:
                print("Error code 1")

        await admin_tools.make_an_annoucment(message = message, state = state, bot = bot)
        await admin_tools.open_main_admin_tools(message = message, state = state)
        await admin_tools.verification(message = message, state = state)
                
        await groups.check(message = message)

def launch_callbacks(dp: aiogram.Dispatcher, bot: aiogram.Bot):
        
        @dp.callback_query()

        async def callback_handler(callback: types.CallbackQuery, state: context.FSMContext):
            print("launch callback")
            await admin_tools.handle_admin_keyboard(callback = callback, state = state)
            await admin_tools.verification_callbacks(callback = callback, state = state, bot = bot, dp = dp)
            
            
        