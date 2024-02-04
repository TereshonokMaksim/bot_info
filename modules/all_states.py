from aiogram.fsm import state

class BasicStates(state.StatesGroup):
    none_state = state.State()
    starting = state.State()
    reg_or_auto = state.State()
    registration = state.State()
    authorization = state.State()
    awaiting = state.State()
    application = state.State()

# class SendStates(state.StatesGroup):
#     theme = state.State()
#     content = state.State()
#     end = state.State()
#     creating_inline_keyboard = state.State()
#     confirming = state.State()

# class VerificationStates(state.StatesGroup):
#     verif_page = state.State()
#     user_verif_page = state.State()
#     confirm_verif = state.State()

class AdminStates(state.StatesGroup):
    admin_awaiting = state.State()
    verif_page = state.State()
    send_new_message = state.State()