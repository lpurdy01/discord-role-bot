# Role Acting Discord Bot
This is a gpt-4 or gpt-3.5-turbo discord bot that will act in accordance to a specified role. The example system is as 
a kawaii programmer doggo, but you can customize that to your liking. 

![doggo](doggo.png)

## Setup
1. Clone the repository
2. Install the requirements
3. Create a discord bot and add it to your server
4. Change `example.env` to `.env` and fill in the values
5. Change `example.config.json` to `config.json` and fill in the values
6. Run `bot/gpt4-discord-bot.py` with the working directory as the root of the repository. 

## Optional deployment to fly.io
1. Create a fly.io account
2. Install the flyctl cli
3. Run `flyctl init` and follow the instructions. It should detect the pregenerated fly.toml and dockerfile, but if it doesn't you have problems.
4. Run `flyctl deploy` and follow the instructions


_Watch your token usage. This does cost money_