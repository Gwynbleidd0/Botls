from getpass import getpass
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, Channel
from telethon.errors import SessionPasswordNeededError
from telethon import TelegramClient, sync
from time import sleep
import json
from collections import defaultdict
import settings as s


def default_value():
    return []


my_chats = {}
chat_serial = {}
configs = defaultdict(default_value)
monitor_config = []
users = []
chats = []
id_name = {}


client = TelegramClient("session", s.api_id, s.api_hash)

client.start()

last_date = None
chunk_size = 20
test = client.get_me()
print(test)
dialogs = client.get_dialogs(limit=200)
i = 0
for d in dialogs:
    if isinstance(d.entity, Channel):
        i += 1
        chat = d.entity
        title = chat.title
        my_chats[i] = title
        chat_id = int("-100{}".format(chat.id))
        id_name[chat_id] = "<<<{}>>>\n\n".format(title)
        chat_serial[i] = chat_id
        print("{}. {} (Id: {})".format(i, title, chat_id).encode('ascii', 'ignore').decode('ascii'))

total = i


def ask_config(i, type):
    while True:
        try:
            if type == "FROM":
                serial = int(input("SOURCE: Enter serial number OF CHAT to GET MESSAGE FROM: "))
            else:
                serial = int(input("DESTINATION: Enter serial number of CHAT to SEND MESSAGE TO: "))
        except ValueError:
            print("Valid value: Integer between 1 to {}".format(i))
            continue
        else:
            if 0 < serial <= i:
                break
            else:
                print("It can be between 1 to {}".format(i))
    return serial


while True:
    try:
        no_of_combination = int(input("How many forward combinations to configure: "))
    except ValueError:
        print("Please enter only integer...")
        continue
    else:
        if no_of_combination > 0:
            break

my_config = "Below is your set configurations:\n\n"

for i in range(1, no_of_combination + 1):
    from_group = ask_config(total, "FROM")
    to_chat = ask_config(total, "TO")

    from_id = chat_serial[from_group]
    to_id = chat_serial[to_chat]

    my_config += "{}. {} - {}\n".format(i, my_chats[from_group], my_chats[to_chat])
    configs[from_id].append(to_id)

print(my_config.encode('ascii', 'ignore').decode('ascii'))

with open("forward_config.txt", "w", encoding="utf8") as f:
    json.dump(configs, f, ensure_ascii=False)

client.disconnect()
