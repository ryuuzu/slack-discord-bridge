
# Slack and Discord Bridge

This is a slack and discord bridge for those who want to connect their slack and discord channels.



## Features

- Link and Auto-create commands.
- Run only one script, if only only one bridge is needed (Commands aren't available for slack.)


  
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`SLACK_BOT_TOKEN=Bot  Token of your slack application.`
`DISCORD_BOT_TOKEN=Bot Token of your discord application.`

  
## Setup Guide

To setup this bridge, you will need a [Discord Application](https://discord.com/developers/applications) and a [Classic Slack Application](https://api.slack.com/apps?new_classic_app=1).

- Add a bot for both slack and discord application after creation.
- Then, add the bots to your respective workspace and server.
- For Slack Bot Scopes, make sure you have `users:read`, `chat:write` and `channels:read` added.
- For Discord Bot Scopes, just give them administrator and they will work fine.
- Do not forget to add the slack bot to the channels you want them to bridge.

Then, run the scripts.
    
## Authors

- [@ryuuzu](https://github.com/ryuuzu)

  
