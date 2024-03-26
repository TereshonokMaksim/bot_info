#PARKING SUPER FREE NO SCAM!!! skachat brawl stars bez virusov besplatno pro max no registration and sms or mms
import modules.account as account
import modules.groups as groups
import modules.admin_tools as admin_tools
import modules.messages as messages
import modules.profile as profile
import aiogram
from aiogram import types
from aiogram.fsm import context
from modules.all_states import BasicStates, AdminStates
import modules.new_message as new_message

def launcher(dp: aiogram.Dispatcher, bot: aiogram.Bot):
    
    @dp.message()

    async def runner(message: types.Message, state: context.FSMContext):
        
        if message.text != None:
            text = message.text.lower()
        else:
            text = " "

        current_state = await state.get_state()
        print(current_state, message.text)

        # print("????")
        await new_message.add_id(message_id = message.message_id, state = state)
        # print("????????????????????????????????????????????????????????????????")
        possible_leave_states = [BasicStates.application, BasicStates.awaiting, AdminStates.admin_awaiting, AdminStates.verif_page, AdminStates.send_new_message]
        if text not in ("/cancel", "/leave"):
            if current_state == BasicStates.starting:
                await account.enter(message = message, state = state)

            # elif current_state == BasicStates.profile:
            elif text == "/profile":
                await profile.open_profile(state = state, message = message, bot = bot)
                
            elif current_state == BasicStates.reg_or_auto:  
                await account.author_or_reg(message = message, state = state)  

            elif current_state == BasicStates.registration:
                await account.registration_(message = message, state = state, bot = bot, dp = dp)

            elif current_state == BasicStates.authorization:
                await account.authorization_(message = message, state = state, bot = bot)

            elif current_state == AdminStates.admin_awaiting:
                await admin_tools.open_main_admin_tools(message = message, state = state)

            elif current_state == AdminStates.verif_page:
                await admin_tools.verification(message = message, state = state, bot = bot)

            elif current_state == BasicStates.application:
                await admin_tools.application_checker(message = message, state = state, bot = bot)

            elif current_state == BasicStates.profile:
                await profile.change_acc_info(message = message, state = state, bot = bot)

            else:
                # print("a")
                try:
                    # print("wth")
                    if message.text.lower() == "/start":
                        # print("wtf")
                        await account.start(message = message, state = state)
                except:
                    print("Error code 1")

            await messages.edit_message_handler(message = message, state = state, bot = bot, dp = dp)

        

        elif text == "/leave":
            if current_state in possible_leave_states:
                await account.leave_account(message = message, state = state, bot = bot)

        elif text == "/cancel":
            await account.cancel(message = message, state = state, bot = bot)

        await groups.check(message = message)

def launch_callbacks(dp: aiogram.Dispatcher, bot: aiogram.Bot):
        
        @dp.callback_query()

        async def callback_handler(callback: types.CallbackQuery, state: context.FSMContext):
            print("launch callback")
            await admin_tools.handle_admin_keyboard(callback = callback, state = state, bot = bot)
            await admin_tools.verification_callbacks(callback = callback, state = state, bot = bot, dp = dp)
            await messages.processing_callbacks_group_messages(callback = callback, state = state)
            await messages.callback_edit_message_handler(callback = callback, state = state, bot = bot, dp = dp)
            await messages.delay_callbac_handler(callback = callback, state = state, bot = bot)
            await profile.callback_profile(callback = callback, state = state, bot = bot)
            
        