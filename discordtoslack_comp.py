import os
from slack_sdk.web import WebClient
from dotenv import load_dotenv

# Loading the .env file vars.
load_dotenv()
SLACK_TOKEN = os.environ.get('SLACK_BOT_TOKEN')

class SlackClient:
    def __init__(self, bot_token) -> None:
        self.client = WebClient(token=bot_token)

    def send(self, channel, message):
        response = self.client.chat_postMessage(channel=channel, text=message)
    
    def getChannelsList(self) -> list:
        channel_list = []
        channel = {}
        channel_payload = self.client.conversations_list()
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
    slack = SlackClient(SLACK_TOKEN)
    for x in slack.getChannelsList():
        print(x)
        print('---------------------------')