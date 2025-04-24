import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
import random
from datetime import datetime
from pytz import timezone
from . import aruby, capsify, sudo_filter, guess_watcher, nopvt, app, collection, limit, user_collection

from .block import block_dec

active_guesses = {}
COOLDOWN_TIME = 30
cooldown_users = {}
GUESS_TIMEOUT = 60

async def get_random_character():
    all_characters = await collection.find({}).to_list(length=None)
    return random.choice(all_characters)

@app.on_message(filters.command("guess"))
@block_dec
async def guess(client, message: Message):
    chat_id = message.chat.id

    if chat_id in active_guesses:
        await message.reply_text(capsify("A guessing game is already running in this chat!"))
        return

    character = await get_random_character()

    active_guesses[chat_id] = {
        'character': character,
        'start_time': datetime.now(),
        'guessed': False,
        'message_id': message.id  
    }

    await message.reply_photo(
        photo=character['img_url'],
        caption=capsify("Guess the character's name! First one to guess correctly wins 20-30 Ruby!")
    )

    asyncio.create_task(check_timeout(client, message, chat_id))

@app.on_message(~filters.me, group=guess_watcher)
async def check_guess(client, message: Message):
    chat_id = message.chat.id

    if not message.from_user:
        return

    user_id = message.from_user.id

    if chat_id not in active_guesses:
        return

    game_data = active_guesses[chat_id]

    if game_data['guessed']:
        return

    if not message.text:
        return

    answer = message.text.strip().lower()

    if user_id in cooldown_users:
        remaining_time = COOLDOWN_TIME - (datetime.now() - cooldown_users[user_id]).total_seconds()
        if remaining_time > 0:
            return

    correct_name = game_data['character']['name'].lower()
    name_parts = correct_name.split()

    if any(part in answer for part in name_parts):
        game_data['guessed'] = True
        reward = random.randint(20, 30)

        await aruby(user_id, reward)

        await message.reply_text(
            capsify(f"Congratulations {message.from_user.first_name}! 🎉 You guessed correctly and won {reward} Ruby!")
        )

        del active_guesses[chat_id]

        cooldown_users[user_id] = datetime.now()

        asyncio.create_task(remove_cooldown(user_id))

    else:
        return

@app.on_message(filters.command("xguess") & sudo_filter)
@block_dec
async def xguess(client, message: Message):
    chat_id = message.chat.id

    if chat_id in active_guesses:
        del active_guesses[chat_id]
        await message.reply_text(capsify("The current guessing game has been terminated."))
    else:
        await message.reply_text(capsify("There is no active guessing game to terminate."))

async def check_timeout(client, message: Message, chat_id):
    await asyncio.sleep(GUESS_TIMEOUT)

    if chat_id in active_guesses and not active_guesses[chat_id]['guessed']:
        character = active_guesses[chat_id]['character']
        original_message_id = active_guesses[chat_id]['message_id']

        await message.reply_text(
            capsify(f"Time out! ⌛ The correct name was: {character['name']}"),
            reply_to_message_id=original_message_id  
        )
        del active_guesses[chat_id]

async def remove_cooldown(user_id):
    await asyncio.sleep(COOLDOWN_TIME)
    if user_id in cooldown_users:
        del cooldown_users[user_id]