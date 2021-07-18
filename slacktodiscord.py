import os
from requests import post
from json import dumps
from bot_setup import setup
from slack_sdk.rtm_v2 import RTMClient
from extras import loadfile
from dotenv import load_dotenv

setup()
# Loading the .env file vars.
load_dotenv()


class SlackRTMClient(RTMClient):
    def send(self, channel, message):
        response = self.web_client.chat_postMessage(
            channel=channel, text=message)

    def getChannelsList(self) -> list:
        channel_list = []
        channel = {}
        channel_payload = self.web_client.conversations_list()
        channel_list_raw = channel_payload['channels']
        for channel_raw in channel_list_raw:
            if channel_raw['is_channel']:
                channel['id'] = channel_raw['id']
                channel['name'] = channel_raw['name']
                channel['description'] = channel_raw['purpose']['value']
                channel_list.append(channel)
                channel = {}
            else:
                continue
        return channel_list


if __name__ == "__main__":
    channelLinks: dict = loadfile('channels.json')

    DISCORD_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
    BASE_MESSAGE_URL = "https://discord.com/api/channels/{0}/messages"

    headers = {"Authorization": f"Bot {DISCORD_TOKEN}",
               "Content-Type": "application/json"}
    rtm = SlackRTMClient(token=os.environ.get('SLACK_BOT_TOKEN'))

    @rtm.on("message")
    def handle(client: RTMClient, event: dict):
        user = event['user']
        userinf = client.web_client.users_info(user=user)
        if not(userinf['user']['is_bot']):
            channel_id = event['channel']
            name = userinf['user']['real_name']
            content = event['text']
            payload = dumps({"content": f"**[SLACK]** *{name}*: {content}"})
            for channelLink in channelLinks:
                if channelLink['slack'] == channel_id:
                    r = post(BASE_MESSAGE_URL.format(channelLink['discord']), headers=headers, data=payload)
                else:
                    continue
    print("Initiating RTM connection.")
    rtm.start()
