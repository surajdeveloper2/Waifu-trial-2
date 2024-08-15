import urllib.request
from pymongo import ReturnDocument
import os
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from shivu import application, sudo_users, CHARA_CHANNEL_ID, SUPPORT_CHAT
from gridfs import GridFS 
from shivu import collection, user_collection, db
from io import BytesIO

WRONG_FORMAT_TEXT = """Wrong ❌ format...  eg. /yadd Img_url muzan-kibutsuji Demon-slayer 3

img_url character-name anime-name rarity-number

use rarity number accordingly rarity Map

rarity_map = {1: "🍀 𝙍𝙖𝙧𝙚", 2: "✨ 𝙇𝙚𝙜𝙚𝙣𝙙𝙖𝙧𝙮", 3: "🪽 𝘾𝙚𝙡𝙚𝙨𝙩𝙞𝙖𝙡", 4: "🥵 𝙀𝙧𝙤𝙩𝙞𝙘", 5: "🐉 𝙈𝙮𝙩𝙝𝙞𝙘𝙖𝙡", 6: "🎴 𝘾𝙤𝙨𝙥𝙡𝙖𝙮", 7: "🔮 𝙇𝙞𝙢𝙞𝙩𝙚𝙙"} """



async def get_next_sequence_number(sequence_name):
    sequence_collection = db.sequences
    sequence_document = await sequence_collection.find_one_and_update(
        {'_id': sequence_name}, 
        {'$inc': {'sequence_value': 1}}, 
        return_document=ReturnDocument.AFTER
    )
    if not sequence_document:
        await sequence_collection.insert_one({'_id': sequence_name, 'sequence_value': 0})
        return 0
    return sequence_document['sequence_value']


async def check(update: Update, context: CallbackContext) -> None:    
    try:
        args = context.args
        if len(context.args) != 1:
            await update.message.reply_text('Incorrect format. Please use: /check id')
            return
            
        character_id = context.args[0]
        
        character = await collection.find_one({'id': args[0]}) 
            
        if character:
            # If character found, send the information along with the image URL
            message = f"<b>Character Name:</b> {character['name']}\n" \
                      f"<b>Anime Name:</b> {character['anime']}\n" \
                      f"<b>Rarity:</b> {character['rarity']}\n" \
                      f"<b>ID:</b> {character['id']}\n"

            if 'img_url' in character:
                await context.bot.send_photo(chat_id=update.effective_chat.id,
                                             photo=character['img_url'],
                                             caption=message,
                                             parse_mode='HTML')
            elif 'vid_url' in character:
                await context.bot.send_video(chat_id=update.effective_chat.id,
                                             video=character['vid_url'],
                                             caption=message,
                                             parse_mode='HTML')
        else:
             await update.message.reply_text("Character not found.")
    except Exception as e:
        await update.message.reply_text(f"Error occurred: {e}")

async def delete(update: Update, context: CallbackContext) -> None:
    if str(update.effective_user.id) not in sudo_users:
        await update.message.reply_text('Ask my Owner to use this Command...')
        return

    try:
        args = context.args
        if len(args) != 1:
            await update.message.reply_text('Incorrect format... Please use: /delete ID')
            return

        
        character = await collection.find_one_and_delete({'id': args[0]})
        if character:
            
            
            await update.message.reply_text('DONE')
        else:
            await update.message.reply_text('Deleted Successfully from db, but character not found In Channel')
    except Exception as e:
        await update.message.reply_text(f'{str(e)}')


async def update(update: Update, context: CallbackContext) -> None:
    if str(update.effective_user.id) not in sudo_users:
        await update.message.reply_text('You do not have permission to use this command.')
        return

    try:
        args = context.args
        if len(args) != 3:
            await update.message.reply_text('Incorrect format. Please use: /update id field new_value')
            return

        # Get character by ID
        character = await collection.find_one({'id': args[0]})
        if not character:
            await update.message.reply_text('Character not found.')
            return

        # Check if field is valid
        valid_fields = ['img_url', 'name', 'anime', 'rarity']
        if args[1] not in valid_fields:
            await update.message.reply_text(f'Invalid field. Please use one of the following: {", ".join(valid_fields)}')
            return

        # Update field
        if args[1] in ['name', 'anime']:
            new_value = args[2].replace('-', ' ').title()
        elif args[1] == 'rarity':
            rarity_map = {1: "🍀 𝙍𝙖𝙧𝙚", 2: "✨ 𝙇𝙚𝙜𝙚𝙣𝙙𝙖𝙧𝙮", 3: "🪽 𝘾𝙚𝙡𝙚𝙨𝙩𝙞𝙖𝙡", 4: "🥵 𝙀𝙧𝙤𝙩𝙞𝙘", 5: "🐉 𝙈𝙮𝙩𝙝𝙞𝙘𝙖𝙡", 6: "🎴 𝘾𝙤𝙨𝙥𝙡𝙖𝙮", 7: "🔮 𝙇𝙞𝙢𝙞𝙩𝙚𝙙"}
            try:
                new_value = rarity_map[int(args[2])]
            except KeyError:
                await update.message.reply_text('Invalid rarity. Please use 1, 2, 3, 4, or 5.')
                return
        else:
            new_value = args[2]

        await collection.find_one_and_update({'id': args[0]}, {'$set': {args[1]: new_value}})

        
        if args[1] == 'img_url':
            
            message = await context.bot.send_photo(
                chat_id=CHARA_CHANNEL_ID,
                photo=new_value,
                caption=f'<b>Character Name:</b> {character["name"]}\n<b>Anime Name:</b> {character["anime"]}\n<b>Rarity:</b> {character["rarity"]}\n<b>ID:</b> {character["id"]}\nUpdated by <a href="tg://user?id={update.effective_user.id}">{update.effective_user.first_name}</a>',
                parse_mode='HTML'
            )
            character['message_id'] = message.message_id
            await collection.find_one_and_update({'id': args[0]}, {'$set': {'message_id': message.message_id}})
        else:
            
            await context.bot.edit_message_caption(
                chat_id=CHARA_CHANNEL_ID,
                message_id=character['message_id'],
                caption=f'<b>Character Name:</b> {character["name"]}\n<b>Anime Name:</b> {character["anime"]}\n<b>Rarity:</b> {character["rarity"]}\n<b>ID:</b> {character["id"]}\nUpdated by <a href="tg://user?id={update.effective_user.id}">{update.effective_user.first_name}</a>',
                parse_mode='HTML'
            )

        await update.message.reply_text('Updated Done in Database.... But sometimes it Takes Time to edit Caption in Your Channel..So wait..')
    except Exception as e:
        await update.message.reply_text(f'I guess did not added bot in channel.. or character uploaded Long time ago.. Or character not exits.. orr Wrong id')

        

async def check_total_characters(update: Update, context: CallbackContext) -> None:
    try:
        total_characters = await collection.count_documents({})
        
        await update.message.reply_text(f"Total number of characters: {total_characters}")
    except Exception as e:
        await update.message.reply_text(f"Error occurred: {e}")


async def add_sudo_user(update: Update, context: CallbackContext) -> None:
    if int(update.effective_user.id) == 6257270528:  # Replace OWNER_ID with the ID of the bot owner
        if update.message.reply_to_message and update.message.reply_to_message.from_user:
            new_sudo_user_id = str(update.message.reply_to_message.from_user.id)
            if new_sudo_user_id not in sudo_users:
                sudo_users.append(new_sudo_user_id)
                await update.message.reply_text("User added to sudo users.")
            else:
                await update.message.reply_text("User is already in sudo users.")
        else:
            await update.message.reply_text("Please reply to a message from the user you want to add to sudo users.")
    else:
        await update.message.reply_text("You are not authorized to use this command.")

ADD_SUDO_USER_HANDLER = CommandHandler('add_sudo_user', add_sudo_user, block=False)
application.add_handler(ADD_SUDO_USER_HANDLER)
       
        

ADD_SUDO_USER_HANDLER = CommandHandler('addsudo', add_sudo_user, block=False)
application.add_handler(ADD_SUDO_USER_HANDLER)

        
application.add_handler(CommandHandler("total", check_total_characters))



DELETE_HANDLER = CommandHandler('ddel', delete, block=False)
application.add_handler(DELETE_HANDLER)
UPDATE_HANDLER = CommandHandler('dupt', update, block=False)
application.add_handler(UPDATE_HANDLER)
CHECK_HANDLER = CommandHandler('dcheck', check, block=False)
application.add_handler(CHECK_HANDLER)
