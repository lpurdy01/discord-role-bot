import discord
import openai
from dotenv import load_dotenv
from discord import app_commands
from configparser import ConfigParser
import os
import json

load_dotenv()

config_file = "config.ini"
config = ConfigParser(interpolation=None)
config.read(config_file)

SERVER_ID = config["discord"]["server_id"]
DISCORD_API_KEY = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

GUILD = discord.Object(id=SERVER_ID)

HISTORY_LENGTH = config["bot"]["history_length"]

ROLE_FILE = config["bot"]["role_file"]

with open(ROLE_FILE, "r") as role_file:
    role_data = json.load(role_file)

SYSTEM_MESSAGE = role_data["SYSTEM_MESSAGE"]
PROMPT_STRUCTURE = role_data["PROMPT_STRUCTURE"]
CONVERSATION_LEAD_IN = role_data["CONVERSATION_LEAD_IN"]

TRIGGER_LIST_FILE = config["bot"]["trigger_list_file"]

with open(TRIGGER_LIST_FILE, "r") as trigger_list_file:
    trigger_list = json.load(trigger_list_file)


def trim_conversation_history(history, max_length=int(HISTORY_LENGTH)):
    if len(history) > max_length + 1:  # Add 1 to account for the system message
        history = [history[0]] + history[-max_length:]  # Keep the system message and last max_length messages
    return history


class Client(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.conversation_history = []
        self.conversation_started = False

    def start_conversation(self, author_display_name):
        self.conversation_history = [{"role": "system",
                                      "content": SYSTEM_MESSAGE}] + CONVERSATION_LEAD_IN

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

        # Respond only when the bot is mentioned or a trigger word is detected
        if not (self.user.mentioned_in(message) or any(
                trigger_word.lower() in input_content.lower() for trigger_word in trigger_list)):
            return

        if not self.conversation_started:
            self.start_conversation(author.display_name)
            self.conversation_started = True

        user_prompt = self.construct_prompt(author, input_content)
        self.conversation_history.append({"role": "user", "content": user_prompt})
        self.conversation_history = trim_conversation_history(self.conversation_history)

        try:
            await message.channel.typing()
            loading_message = await message.channel.send("Typing...")
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=self.conversation_history
            )

            assistant_response = response["choices"][0]["message"]["content"]
            self.conversation_history.append({"role": "assistant", "content": assistant_response})
            self.conversation_history = trim_conversation_history(self.conversation_history)

        except AttributeError:
            assistant_response = "It looks like you might have to update your openai package. You can do that with ```pip install --upgrade openai```"
        except ImportError:
            assistant_response = "You might not have all required packages installed. Make sure you install the openai and discord package"
        except openai.error.AuthenticationError:
            assistant_response = "It looks like you don't have access to the gpt-4 model. Please make sure you have been invited by openai and double check your openai API key and organization ID"
        except openai.error.RateLimitError:
            assistant_response = "Your rate has been limited. This might be because of too many requests or because your rate limit has been reached."
        except openai.error.Timeout:
            assistant_response = "My response is taking too long and I have received a timeout error."
        except openai.error.APIConnectionError:
            assistant_response = "I can't connect to the OpenAI servers at the moment. Please try again later!"

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

openai.api_key = OPENAI_API_KEY
openai.Model.list()

client.run(DISCORD_API_KEY)
