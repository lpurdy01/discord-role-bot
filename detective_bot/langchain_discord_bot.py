import discord
from dotenv import load_dotenv
from discord import app_commands
from configparser import ConfigParser
import os
import json
from conversation_agent_with_search_test import init_agent

load_dotenv()

config_file = "../detective_bot/config.ini"
config = ConfigParser(interpolation=None)
config.read(config_file)

SERVER_ID = config["discord"]["server_id"]
DISCORD_API_KEY = os.getenv("BOT_TOKEN")

GUILD = discord.Object(id=SERVER_ID)

ROLE_FILE = config["bot"]["role_file"]

with open(ROLE_FILE, "r") as role_file:
    role_data = json.load(role_file)

PROMPT_STRUCTURE = role_data["PROMPT_STRUCTURE"]

TRIGGER_LIST_FILE = config["bot"]["trigger_list_file"]

with open(TRIGGER_LIST_FILE, "r") as trigger_list_file:
    trigger_list = json.load(trigger_list_file)


class Client(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.conversation_history = []
        self.conversation_started = False
        self.agent_chain = None

    def start_conversation(self):
        self.agent_chain = init_agent()

    def construct_prompt(self, author, message_content):
        return PROMPT_STRUCTURE.format(user=author, prompt=message_content)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=GUILD)
        await self.tree.sync(guild=GUILD)

    async def on_message(self, message):
        author = message.author

        if message.author == self.user:
            return

        input_content = message.content
        print(f"{message.author}: {input_content}")

        if not (self.user.mentioned_in(message) or any(
                trigger_word.lower() in input_content.lower() for trigger_word in trigger_list)):
            return

        if not self.conversation_started:
            self.start_conversation()
            self.conversation_started = True

        user_prompt = self.construct_prompt(author, input_content)

        try:
            await message.channel.typing()
            loading_message = await message.channel.send("Typing...")

            output = self.agent_chain.run(input=user_prompt)
            assistant_response = output


        except Exception as e:
            assistant_response = f"An error occurred: {str(e)}"

        if assistant_response is not None:
            parts = [assistant_response[i:i + 2000] for i in range(0, len(assistant_response), 2000)]
            for index, part in enumerate(parts):
                try:
                    print(f"GPT: {part}")
                    await loading_message.delete()
                    await message.channel.send(part)
                except discord.errors.Forbidden:
                    print("GPT: I am not able to send a message. Do I have the correct permissions on your server?")


gpt4_intents = discord.Intents.default()
gpt4_intents.messages = True
gpt4_intents.message_content = True
client = Client(intents=gpt4_intents)

client.run(DISCORD_API_KEY)