import modules.all_states as all_states
import aiogram.filters as filters
import aiogram.types as types
from modules.data_work import edit_database

async def check(message: types.Message):
    print("check launch")
    if message.content_type == types.ContentType.NEW_CHAT_MEMBERS:
        print(message.new_chat_members[0].username)
        # if message.new_chat_members[0].username == "InformatorTeam2Bot":
        print(2)
        # print(edit_database(command = "SELECT group_id FROM data"))
        try:
            data = edit_database(command = "SELECT group_id FROM data")[-1][-1].split(",")
        except:
            data = ""
        if str(message.chat.id) not in data:
            edit_database(command = f"UPDATE data SET group_id = '{','.join(data)},{message.chat.id}'")
    if message.content_type == types.ContentType.LEFT_CHAT_MEMBER:
        if message.left_chat_member.username == "InformatorTeam2Bot":
            try:
                data = edit_database(command = "SELECT group_id FROM data")[-1][-1].split(",")
            except:
                data = ""
            print(data, message.chat.id)
            if str(message.chat.id) in data:
                data.remove(str(message.chat.id))
                edit_database(command = f"UPDATE data SET group_id = '{','.join(data)}'")