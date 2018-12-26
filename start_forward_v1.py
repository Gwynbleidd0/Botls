from telethon.tl.functions.messages import ForwardMessagesRequest,SendMessageRequest
from telethon import TelegramClient, events
import settings as s
import json
import time


try:
    with open("forward_config.txt", encoding="utf8") as f:
        combinations = json.load(f)
except:
    input("Press enter to exit the script: ")
    exit()


channels = []
print(combinations)

for chat in list(combinations.keys()):
    if chat.startswith("-100"):
        channels.append(int(chat))
print(channels)
client = TelegramClient("session", api_hash=s.api_hash, api_id=s.api_id)



@client.on(events.NewMessage())
async def my_event_handler(event: events.NewMessage.Event):
    sender = "-100{}".format(event.message.chat.id)
    print(sender)
    for destination in combinations[sender]:
        try:
            print(event.message.message)
            await client(SendMessageRequest(
            peer=destination,
            message=event.message.message
            ))
        except Exception as e:
            print(e)


with client.start():
    print('(Press Ctrl+C to stop this)')
    client.run_until_disconnected()
