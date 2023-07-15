from pyrogram.enums import ChatMemberStatus
from pyrogram import Client, filters
from ForceSubscribeBot.admin_check import admin_check
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from ForceSubscribeBot.database.chats_sql import get_action, get_ignore_service, get_only_owner, chat_exists
from Config import START_IMG

@Client.on_message(filters.text  & filters.command("settings"))
async def settings(bot: Client, msg):
    success = await admin_check(bot, msg)
    if not success:
        return
    chat_id = msg.chat.id
    if not await chat_exists(msg.chat.id):
        await msg.reply("Please add a force subscribe chat using /fsub to use me.")
        return
    only_owner = await get_only_owner(chat_id)
    creator = True if (await bot.get_chat_member(chat_id, msg.from_user.id)).status==ChatMemberStatus.OWNER  else False
    if only_owner and not creator:
        await msg.reply("Only the owner can change settings in this chat.")
        return
    buttons = await action_markup(chat_id)
    await msg.reply_photo(START_IMG,
        caption="Settings:\n\n"
        "1) Choose action type for those who haven't joined the force subscribe chat. Defaults to mute.\n"
        "2) Choose to ignore welcome messages or not. If you don't want the bot to take action on users just when the chat (didn't chat) chooses on else, off antispam y.\n"
        "3) Choose to allow admins to change fsub and settings or not. Defaults to 'allow only'.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


async def action_markup(chat_id):
    action = await get_action(chat_id)
    warn = "Warn"
    mute = "Mute"
    kick = "Kick"
    ban = "Ban"
    if action == "mute":
        mute += " ✅"
    elif action=="warn":
        warn+="✅"
    elif action == "kick":
        kick += " ✅"
    else:
        ban += " ✅"
    ignore_service = await get_ignore_service(chat_id)
    ignore_service_text = "Ignore Welcome Message: "
    if ignore_service:
        ignore_service_text += "On"
        data = "on"
    else:
        ignore_service_text += "Off"
        data = "off"
    only_owner = await get_only_owner(chat_id)
    if only_owner:
        only_owner = "Allow Only Owner"
        data2 = "True"
    else:
        only_owner = "Allow Admins Too"
        data2 = "False"
    buttons = [
        [
            InlineKeyboardButton(warn, callback_data=f"action+warn+{chat_id}"),
            InlineKeyboardButton(mute, callback_data=f"action+mute+{chat_id}"),
            InlineKeyboardButton(kick, callback_data=f"action+kick+{chat_id}"),
            InlineKeyboardButton(ban, callback_data=f"action+ban+{chat_id}")
        ],
        [
            InlineKeyboardButton(ignore_service_text, callback_data=f"action+{data}+{chat_id}")
        ],
        [
            InlineKeyboardButton(only_owner, callback_data=f"action+{data2}+{chat_id}")
        ]
    ]
    return buttons
