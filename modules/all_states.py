from aiogram.fsm import state

class BasicStates(state.StatesGroup):
    none_state = state.State()
    starting = state.State()
    reg_or_auto = state.State()
    registration = state.State()
    authorization = state.State()
    awaiting = state.State()
    application = state.State()
    profile = state.State()

class SendStates(state.StatesGroup):
    time = state.State()
    image = state.State()
    description = state.State()
    product = state.State()
    edit = state.State()

# class VerificationStates(state.StatesGroup):
#     verif_page = state.State()
#     user_verif_page = state.State()
#     confirm_verif = state.State()

class AdminStates(state.StatesGroup):
    admin_awaiting = state.State()
    verif_page = state.State()
    send_new_message = state.State()