import os
import discord
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
from bot_setup import setup
from extras import loadfile, writefile
from slacktodiscord import SlackRTMClient

# Creates required files
setup()

# Loading the .env file vars.
load_dotenv()
DISCORD_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
SLACK_TOKEN = os.environ.get('SLACK_BOT_TOKEN')

rtm_client = SlackRTMClient(token=SLACK_TOKEN)

# Loading JSON Datas
channelLinks:dict = loadfile('channels.json')

discord_bot = commands.Bot(command_prefix=".")

@discord_bot.event
async def on_ready():
    print("The bot is ready.")

@discord_bot.event
async def on_message(message: discord.Message):
    channel = message.channel
    author = message.author
    content = message.content
    message_to_send = f"*[DISCORD]* _{author}_: {content}"
    if not(author.bot) and not(content.startswith("DNB")):
        for channelLink in channelLinks:
            if channelLink['discord'] == str(channel.id):
                rtm_client.send(channelLink['slack'], message_to_send)
            else:
                continue

@commands.has_guild_permissions(administrator=True)
@discord_bot.command(help="List all the channels from slack.", brief="Useful for `link`", aliases=['lsc'])
async def listslackchannels(ctx):
    channels = "The channel list from slack are:"
    for slackChannel in rtm_client.getChannelsList():
        channels += f"\n**ID:** {slackChannel['id']} | **Name:** {slackChannel['name']}"
    await ctx.send(channels)

@commands.has_guild_permissions(administrator=True)
@discord_bot.command(help="Link the active channel with slack's channel", brief="Use `listslackchannels` to get channel names.\nNote: This will overwrite any existing links.")
async def link(ctx, slack_channel_id):
    channel_id = str(ctx.channel.id)
    for channelLink in channelLinks:
        if channelLink['discord'] == channel_id or channelLink['slack'] == slack_channel_id:
            return await ctx.send("This channel has already been linked. Please try another one or clear the existing channel links.")
    slack_channel = rtm_client.web_client.conversations_info(channel=slack_channel_id)
    if not(slack_channel['ok']):
        return await ctx.send("Something went wrong! Make sure the Channel ID is correct.")
    channel_dict = {}
    channel_dict['slack'] = slack_channel_id
    channel_dict['discord'] = str(channel_id)
    channelLinks.append(channel_dict)
    writefile("channels.json", channelLinks)
    await ctx.send(f"This channel has been linked with {slack_channel['channel']['name']}")


@commands.has_guild_permissions(administrator=True)
@discord_bot.command(help="Use this command only if you want to bridge all the Slack Channels with Discord Channels.", brief="For individual channels use `link`.", aliases=['csc'])
async def createslackchannels(ctx):
    slackChannelList = rtm_client.getChannelsList()
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
