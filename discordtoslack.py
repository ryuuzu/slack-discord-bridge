import os
import discord
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
from bot_setup import setup
from extras import loadfile, writefile
from discordtoslack_comp import SlackClient

# Creates required files
setup()

# Loading the .env file vars.
load_dotenv()
DISCORD_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
SLACK_TOKEN = os.environ.get('SLACK_BOT_TOKEN')

# Loading JSON Datas
channelLinks:dict = loadfile('channels.json')

slack = SlackClient(SLACK_TOKEN)
discord_bot = commands.Bot(command_prefix=".")

@discord_bot.event
async def on_ready():
    print("The bot is ready <3")

@discord_bot.event
async def on_message(message: discord.Message):
    channel = message.channel
    author = message.author
    content = message.content
    message_to_send = f"*[DISCORD]* _{author}_: {content}"
    for channelLink in channelLinks:
        if channelLink['discord'] == str(channel.id):
            slack.send(channelLink['slack'], message_to_send)
        else:
            continue
    

@discord_bot.command(aliases=['csc'])
async def createslackchannels(ctx):
    slackChannelList = slack.getChannelsList()
    guild = ctx.guild
    await ctx.send(f"This will take around {len(slackChannelList)} to {len(slackChannelList)*2} seconds.")
    for slackChannel in slackChannelList:
        channel_dict = {}
        if slackChannel['id'] in channelLinks.keys():
            continue
        else:
            new_channel = await guild.create_text_channel(name=slackChannel['name'], topic=slackChannel['description'])
            channel_dict['slack'] = slackChannel['id']
            channel_dict['discord'] = str(new_channel.id)
            channelLinks.append(channel_dict)
            # Sleep for API Calls management
            await asyncio.sleep(1)
    writefile("channels.json", channelLinks)
    await ctx.send("Creating the channels has been completed.")

discord_bot.run(DISCORD_TOKEN)