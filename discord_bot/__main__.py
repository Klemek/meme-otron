import os
import traceback
import logging
import discord
import re
import tempfile
import sys
from datetime import datetime
from dotenv import load_dotenv

from meme_otron import img_factory as imgf
from meme_otron import meme_db as db
from meme_otron import utils
from meme_otron import meme_otron

VERSION = "1.0-dev"
t0 = datetime.now()
logging.basicConfig(format="[%(asctime)s][%(levelname)s][%(module)s] %(message)s", level=logging.INFO)

# Loading token
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

if token is None:
    logging.error("No token was loaded, please verify your .env file")
    sys.exit(1)

imgf.load_fonts()
db.load_memes()

client = discord.Client()

SENT = {}


def debug(message, txt):
    """
    Print a log with the context of the current event

    :param (discord.Message) message: message that triggered the event
    :param (str) txt: text of the log
    """
    logging.info(f"{message.guild} > #{message.channel}: {txt}")


@client.event
async def on_ready():
    """
    Called when client is connected
    """
    # Change status
    await client.change_presence(
        activity=discord.Game(f"v{VERSION}"),
        status=discord.Status.online
    )
    # Debug connected guilds
    logging.info(f'{client.user} v{VERSION} has connected to Discord\nto the following guilds:')
    for guild in client.guilds:
        logging.info(f'- {guild.name}(id: {guild.id})')


async def delete(message):
    """
    TODO

    :param (discord.Message) message:
    :rtype: bool
    """
    try:
        await message.delete()
        return True
    except discord.Forbidden:
        pass
    except discord.NotFound:
        pass
    return False


@client.event
async def on_message(message):
    """
    Called when a message is sent to any channel on any guild

    :param (discord.Message) message: message sent
    """
    # Ignore self messages
    if message.author == client.user:
        return

    direct = message.channel.type == discord.ChannelType.private

    if not direct:
        mid = f'{message.guild.id}/{message.channel.id}/{message.author.id}'
    else:
        mid = message.author.id

    if direct or client.user in message.mentions:
        message.content = re.sub(r'<@[^>]+>', '', message.content).strip()
        args = utils.parse_arguments(message.content)
        debug(message, str(args))
        if len(args) == 0 or args[0].lower().strip() == "help":
            await message.channel.send(f"Hey {message.author.mention},\n"
                                       f"You can generate a meme with the syntax\n"
                                       f"```\n"
                                       f"[template] \"text 1\" \"text 2\" ...\n"
                                       f"```"
                                       f"You can find a more detailed help and a list of templates at:\n"
                                       f"<https://github.com/klemek/meme-otron/tree/master/discord>")
            return
        if len(args) > 0 and args[0].lower().strip() == "delete":
            if mid in SENT and len(SENT[mid]) > 0 and await delete(SENT[mid][-1]):
                if not direct:
                    await delete(message)
            else:
                await message.add_reaction("⚠")
            return
        async with message.channel.typing():
            left_wmark_text = None
            if len(args) > 1 and message.author.display_name is not None:
                left_wmark_text = f"By {message.author.display_name}"
            img = meme_otron.compute(*args, left_wmark_text=left_wmark_text)
            if img is None:
                hint = db.find_nearest(args[0])
                response = f":warning: Template `{args[0]}` not found\n"
                if hint is not None:
                    response += f"Did you mean `{hint}`?\n"
                response += f"You can find a more detailed help and a list of templates at:\n" \
                            f"<https://github.com/klemek/meme-otron/tree/master/docs/README.md>"
                await message.channel.send(response)
            else:
                with tempfile.NamedTemporaryFile(delete=False) as output:
                    img.save(output, format="JPEG")
                    response = None
                    if len(args) == 1:
                        meme = db.get_meme(args[0])
                        response = f"Template `{meme.id}`:"
                        if len(meme.aliases) > 0:
                            response += f"\n- Aliases: `{'`, `'.join(meme.aliases)}`"
                        if meme.info is not None:
                            response += f"\n- More info: <{meme.info}>"
                    elif not direct:
                        response = f"A meme by {message.author.mention}:"
                    if mid not in SENT:
                        SENT[mid] = []
                    response = await message.channel.send(response,
                                                          file=discord.File(filename="meme.jpg", fp=output.name))
                    SENT[mid] += [response]
                    try:
                        os.remove(output.name)
                    except PermissionError:
                        pass
            if not direct:
                await delete(message)

# Launch client and rerun on errors
while True:
    try:
        client.run(token)
        break  # clean kill
    except Exception as e:
        t = datetime.now()
        logging.error(f"Exception raised at {t:%Y-%m-%d %H:%M} : {repr(e)}")
        fileName = f"error_{t:%Y-%m-%d_%H-%M-%S}.txt"
        if os.path.exists(fileName):
            logging.error("Two many errors, killing")
            break
        with open(fileName, 'w') as f:
            f.write(f"Discord AI Dungeon 2 v{VERSION} started at {t0:%Y-%m-%d %H:%M}\r\n"
                    f"Exception raised at {t:%Y-%m-%d %H:%M}\r\n"
                    f"\r\n"
                    f"{traceback.format_exc()}")
