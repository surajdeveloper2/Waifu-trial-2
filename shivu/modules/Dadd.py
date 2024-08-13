from telegraph import upload_file
from pyrogram import filters
from shivu import shivuu, collection
from pyrogram.types import InputMediaPhoto
import os

WRONG_FORMAT_TEXT = """Wrong ❌ format...  eg. /nadd reply to photo muzan-kibutsuji Demon-slayer 3

format:- /nadd reply character-name anime-name rarity-number

use rarity number accordingly rarity Map

rarity_map = {1: "🍀 𝙍𝙖𝙧𝙚", 2: "✨ 𝙇𝙚𝙜𝙚𝙣𝙙𝙖𝙧𝙮", 3: "🪽 𝘾𝙚𝙡𝙚𝙨𝙩𝙞𝙖𝙡", 4: "🥵 𝙀𝙧𝙤𝙩𝙞𝙘", 5: "🐉 𝙈𝙮𝙩𝙝𝙞𝙘𝙖𝙡", 6: "🎴 𝘾𝙤𝙨𝙥𝙡𝙖𝙮", 7: "🔮 𝙇𝙞𝙢𝙞𝙩𝙚𝙙"}
"""

# Channel ID for posting character information (replace with your actual channel ID)
CHARA_CHANNEL_ID = -1002168367599

rarity_map = {1: "🍀 𝙍𝙖𝙧𝙚", 2: "✨ 𝙇𝙚𝙜𝙚𝙣𝙙𝙖𝙧𝙮", 3: "🪽 𝘾𝙚𝙡𝙚𝙨𝙩𝙞𝙖𝙡", 4: "🥵 𝙀𝙧𝙤𝙩𝙞𝙘", 5: "🐉 𝙈𝙮𝙩𝙝𝙞𝙘𝙖𝙡", 6: "🎴 𝘾𝙤𝙨𝙥𝙡𝙖𝙮", 7: "🔮 𝙇𝙞𝙢𝙞𝙩𝙚𝙙"}
async def find_available_id():
    cursor = collection.find().sort('id', 1)
    ids = [doc['id'] for doc in await cursor.to_list(length=None)]
    for i in range(1, max(map(int, ids)) + 2):  # +2 to account for the case where the max ID is the last one
        if str(i).zfill(2) not in ids:
            return str(i).zfill(2)
    return str(max(map(int, ids)) + 1).zfill(2)  # return the next available ID

@shivuu.on_message(filters.command(["uadd"]) & filters.user([7378476666, 1962399469]))
async def ul(client, message):
    reply = message.reply_to_message
    if reply and (reply.photo or reply.document):
        args = message.text.split()
        if len(args) != 4:
            await client.send_message(chat_id=message.chat.id, text=WRONG_FORMAT_TEXT)
            return
        
        character_name = args[1].replace('-', ' ').title()
        anime = args[2].replace('-', ' ').title()
        rarity = int(args[3])
        
        if rarity not in rarity_map:
            await message.reply_text("Invalid rarity value. Please use a value between 1 and 9.")
            return
        
        rarity_text = rarity_map[rarity]
        available_id = await find_available_id()

        character = {
            'name': character_name,
            'anime': anime,
            'rarity': rarity_text,
            'id': available_id
        }

        i = await message.reply("<ᴘʀᴏᴄᴇꜱꜱɪɴɢ>....")
        path = await reply.download()
        try:
            fk = upload_file(path)
            for x in fk:
                url = "https://telegra.ph" + x
                
                # Upload to MongoDB
                character['img_url'] = url
                
                # Send to channel
                sent_message = await client.send_photo(
                    chat_id=CHARA_CHANNEL_ID,
                    photo=url,
                    caption=(
                        f"Character Name: {character_name}\n"
                        f"Anime Name: {anime}\n"
                        f"Rarity: {rarity_text}\n"
                        f"ID: {available_id}\n"
                        f"Added by [{message.from_user.first_name}](tg://user?id={message.from_user.id})"
                    ),
                )
                 
               
                await collection.insert_one(character)
                await message.reply_text('CHARACTER ADDED....')
        except Exception as e:
            await message.reply_text(f"Character Upload Unsuccessful. Error: {str(e)}")
        finally:
            os.remove(path)  # Clean up the downloaded file
    else:
        await message.reply_text("Please reply to a photo or document.")
