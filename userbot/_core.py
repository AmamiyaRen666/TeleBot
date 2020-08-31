from userbot.utils import command, remove_plugin, load_module
from pathlib import Path
import asyncio
import os
import userbot.utils
from datetime import datetime
from .. import ALIVE_NAME 

DELETE_TIMEOUT = 5
thumb_image_path = "./TeleBot.png"
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "Telebot User"

@command(pattern="^.install", outgoing=True)
async def install(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        try:
            downloaded_file_name = await event.client.download_media(  # pylint:disable=E0602
                await event.get_reply_message(),
                "userbot/plugins/"  # pylint:disable=E0602
            )
            if "(" not in downloaded_file_name:
                path1 = Path(downloaded_file_name)
                shortname = path1.stem
                load_module(shortname.replace(".py", ""))
                await event.edit("TeleBot Succesfully Installed The Plugin `{}`".format(os.path.basename(downloaded_file_name)))
            else:
                os.remove(downloaded_file_name)
                await event.edit("TeleBot returned an error! Plugin cannot be installed.")
        except Exception as e:  # pylint:disable=C0103,W0703
            await event.edit(str(e))
            os.remove(downloaded_file_name)
    await asyncio.sleep(DELETE_TIMEOUT)
    await event.delete()

@command(pattern="^.send (?P<shortname>\w+)$", outgoing=True)
async def send(event):
    if event.fwd_from:
        return
    message_id = event.message.id
    thumb = thumb_image_path
    input_str = event.pattern_match["shortname"]
    the_plugin_file = "./userbot/plugins/{}.py".format(input_str)
    start = datetime.now()
    await event.client.send_file(  # pylint:disable=E0602
        event.chat_id,
        the_plugin_file,
        force_document=True,
        allow_cache=False,
        thumb=thumb,
        reply_to=message_id
    )
    end = datetime.now()
    time_taken_in_ms = (end - start).seconds
    await event.edit(f"__**Plugin Name:- {input_str} .**__\n__**Uploaded in {time_taken_in_ms} seconds.**__\n__**Uploaded by :-**__ [{DEFAULTUSER}](tg://user?id={hmm})\n©@TeleBotSupport")
    await asyncio.sleep(DELETE_TIMEOUT)
    await event.delete()

@command(pattern="^.unload (?P<shortname>\w+)$", outgoing=True)
async def unload(event):
    if event.fwd_from:
        return
    shortname = event.pattern_match["shortname"]
    try:
        remove_plugin(shortname)
        await event.edit(f"TeleBot has successfully unloaded {shortname}")
    except Exception as e:
        await event.edit("TeleBot has successfully unloaded {shortname}\n{}".format(shortname, str(e)))

@command(pattern="^.load (?P<shortname>\w+)$", outgoing=True)
async def load(event):
    if event.fwd_from:
        return
    shortname = event.pattern_match["shortname"]
    try:
        try:
            remove_plugin(shortname)
        except:
            pass
        load_module(shortname)
        await event.edit(f"TeleBot has successfully loaded {shortname}")
    except Exception as e:
        await event.edit(f"TeleBot could not load {shortname} because of the following error.\n{str(e)}")
