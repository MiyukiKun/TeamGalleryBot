from telethon import events, Button
from telethon.tl.types import UpdateChannelParticipant
from telethon.tl.functions.channels import GetFullChannelRequest
from config import bot, bot1, main_group_id, main_bot_id
import time
from telethon.tl.types import InputWebDocument as wb
import os
from telegraph import Telegraph, upload_file
from Database.mongo import ChannelsDB, AdsDB, UsersDB
from Helper.helper import parse_arg, parse_about
from datetime import datetime
import asyncio
from telethon.tl.types import PeerUser, PeerChat, PeerChannel


ChannelsDB = ChannelsDB()
AdsDB = AdsDB()
UsersDB = UsersDB()

telegraph = Telegraph()
r = telegraph.create_account(short_name="Anime_Gallery_Manager")
auth_url = r["auth_url"]


@bot1.on(events.Raw(UpdateChannelParticipant))
async def update(event):
    # print(event)
    if event.user_id == main_bot_id:
        channel = await bot1.get_entity(event.channel_id)
        x = await bot1.download_profile_photo(channel)
        media_url = upload_file(x)
        pic = f"https://telegra.ph{media_url[0]}"
        ChannelsDB.add({'_id':channel.id , 'username':channel.username, 'name':channel.title, 'pfp':pic})
        await bot.send_message(main_group_id, f"I just spread My power to {channel.title},  @{channel.username}", file=x)
        os.remove(x)

@bot.on(events.InlineQuery)
async def handler(event):
    builder = event.builder
    channels = ChannelsDB.full()
    options = []          

    for i in channels:
        if (parse_arg(event.text) in parse_arg(i['username'])) or (parse_arg(event.text) in parse_arg(i['name'])):
            channel = await bot1.get_entity(f"t.me/{i['username']}")
            ch_full = await bot1(GetFullChannelRequest(channel=channel))
            pic = i['pfp']
            options.append(builder.article(
                thumb=wb(pic, 0, "image/jpeg", []),
                title = channel.title,
                description = f"@{i['username']}",
                text = f"{parse_about(ch_full.full_chat.about)}\n\n Link [-]({pic}) @{i['username']}"))
            if len(options) >= 5:
                break
    await event.answer(options)
    

@bot.on(events.NewMessage(pattern="/start"))
async def _(event):
    if event.is_private:
        await event.reply("Im a bot specially made for managing @Anime_Gallery, and provide easy access to all channels we have access to", file = "Hepler\AGM.png")
        AdsDB.add({'_id':event.id})

@bot.on(events.NewMessage(pattern='/users', chats=main_group_id))
async def _(event):
    data = AdsDB.full()
    await event.reply(f"There are {len(data)} users we can broadcast to.")

@bot.on(events.NewMessage(pattern='/broadcast', chats=main_group_id))
async def _(event):
    msg = await event.get_reply_message()
    data = AdsDB.full()
    for i in data:
        try:
            await bot.send_message(i['_id'], msg)
        except:
            pass


@bot.on(events.NewMessage(pattern="/ping"))
async def _(event):
    start_time = time.time()
    reply = await event.reply("Pinging...")
    end_time = time.time()
    telegram_ping = str(round((end_time - start_time) * 1000, 3)) + " ms"
    await reply.edit(f"Pong!!\n{telegram_ping}")


@bot.on(events.NewMessage(pattern="/spromote", chats=main_group_id))
async def _(event):
    data = event.raw_text.split(" ")
    user = event.sender_id
    me = await bot1.get_entity(main_bot_id)
    chat = await bot1.get_entity(data[1])
    perms = await bot1.get_permissions(chat, me)
    await bot1.edit_admin(chat, user, change_info=perms.change_info, post_messages= perms.post_messages, edit_messages=perms.edit_messages, delete_messages=perms.delete_messages, invite_users=perms.invite_users, add_admins=perms.add_admins, manage_call=perms.manage_call)
    await event.reply("Promoted")


@bot.on(events.NewMessage(pattern="/sdemote", chats=main_group_id))
async def _(event):
    data = event.raw_text.split(" ")
    user = event.sender_id
    chat = await bot1.get_entity(data[1])
    await bot1.edit_admin(chat, user, change_info=False, post_messages=False, edit_messages=False, delete_messages=False, invite_users=False, add_admins=False, manage_call=False)
    await event.reply("Demoted")


@bot.on(events.NewMessage(pattern=("/addpower"), chats=main_group_id))
async def add_power(event):
    try:
        data = event.raw_text.split(" ")
        channel = await bot1.get_entity(data[1])
        x = await bot1.download_profile_photo(channel)
        media_url = upload_file(x)
        pic = f"https://telegra.ph{media_url[0]}"
        ChannelsDB.add({'_id':channel.id , 'username':channel.username, 'name':channel.title, 'pfp':pic})
        await bot.send_message(-1001361915166, f"I just spread My power to {channel.title},  @{channel.username}", file=x)
        os.remove(x)
    except Exception as e:
        await bot.send_message(main_group_id, str(e))


@bot.on(events.NewMessage(pattern=("/rmpower"), chats=main_group_id))
async def add_power(event):
    try:
        data = event.raw_text.split(" ")
        channel = await bot1.get_entity(data[1])
        ChannelsDB.remove({'_id':channel.id})
        await bot.send_message(-1001361915166, f"I just removed My power from {channel.title},  @{channel.username}")
    except Exception as e:
        await bot.send_message(main_group_id, str(e))


@bot.on(events.NewMessage(pattern=("/power"), chats=main_group_id))
async def power(event):
    channels = ChannelsDB.full()
    string = []
    for i in channels:
        string.append(i['username'])
    string.sort()
    if len(string) < 20:
        string = "\n@".join(string)
        print(string)
        await bot.send_message(main_group_id, f"I have power over\n\n@{string}")
        return
    data = ""
    for i in range(0, 20):
        data = f"{data}\n{i+1}. @{string[i]}"
    await bot.send_message(main_group_id, f"I have power over\n\n{data}", buttons=[Button.inline("Next", data=("page:0:20"))])


@bot.on(events.CallbackQuery(pattern=(b"page:")))    
async def page(event):
    data = event.data.decode('utf-8')
    data_split = data.split(':')
    start = int(data_split[1])
    end = int(data_split[2])
    channels = ChannelsDB.full()
    string = []
    for i in channels:
        string.append(i['username'])
    string.sort()

    if len(string) <= end+20:
        new_end = len(string)
        buttons = [Button.inline("Previous", data=f"page:{start-20}:{end-20}")]
    
    elif start == -20:
        new_end = 20
        buttons = [Button.inline("Next", data=f"page:{end}:{new_end}")]

    else:
        new_end = end+20
        buttons = [Button.inline("Previous", data=f"page:{start-20}:{end-20}"), Button.inline("Next", data=f"page:{end}:{new_end}")]
    data = ""
    for i in range(end, new_end):
        data = f"{data}\n{i+1}. @{string[i]}"

    try:
        await event.edit(f"I have power over\n\n{data}", buttons=buttons)
    except:
        pass


@bot.on(events.NewMessage(pattern="/help", chats=main_group_id))
async def help(event):
    await event.reply("""
    `/start` and `/ping` Just to confirm
    `/spromote <t.me/channel>`
    `/sdemote <t.me/channel>`
    `/power` check total channels bot has power in
    `/rmpower` removes channel from database(does not leave channel)
    `/addpower` adds channel to database(does not join channel)
    `@Name of bot, search anime (inline search)`
    """)


@bot1.on(events.NewMessage())
async def ad(event):
    if event.via_bot_id == 5022774751:
        AdsDB.add({'_id':f"{event.chat_id}:{event.id}", 'time': datetime.now()})


async def del_ad():
    while True:
        ads = AdsDB.full()
        for i in ads:
            if (datetime.now() - i['time']).days >= 1:
                a = i['_id'].split(":")
                try:
                    await bot1.delete_messages(int(a[0]), int(a[1]))
                except:
                    pass
                AdsDB.remove({'_id':i['_id']})
        await asyncio.sleep(300)


@bot.on(events.NewMessage(pattern="/active_ads"))
async def _(event):
    ads = AdsDB.full()
    msg = ''
    for i in ads:
        a = i['_id'].split(":")
        b = a[0].replace("-100", "")
        try:
            channel = await bot1.get_entity(PeerChannel(int(b)))
            msg += f't.me/{channel.username}/{a[1]}\n'
        except Exception as e:
            await event.reply(f"Error:\n{str(e)}")
            msg += f't.me/c/{b}/{a[1]}\n'

    await event.reply(msg, link_preview=False)


loop = asyncio.get_event_loop()

loop.run_until_complete(del_ad())

bot.start()

bot.run_until_disconnected()
