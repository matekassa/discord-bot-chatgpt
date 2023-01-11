import discord
import openai
from decouple import config

DISCORD_TOKEN = config('DISCORD_TOKEN')
OPENAI_API_KEY = config('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY


class DiscordBotClient(discord.Client):

    def __init__(self):
        # adding intents module to prevent intents error in __init__ method in newer versions of Discord.py
        intents = discord.Intents.default(
        )  # Select all the intents in your bot settings as it's easier
        intents.message_content = True
        super().__init__(intents=intents)
        self.api_endpoint = OPENAI_API_KEY

    async def on_ready(self):
        # print out information when the bot wakes up
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        # ignore the message if it comes from the bot itself
        if message.author.id == self.user.id:
            return
        # while the bot is waiting on a response from the model
        # set its status as typing for user-friendliness
        async with message.channel.typing():
            response = generate_message(message)

            # we may get ill-formed response if the model hasn't fully loaded
            # or has timed out
            if not response:
                if 'error' in response:
                    response = '`Error: {}`'.format(response['error'])
                else:
                    response = 'Hmm... something is not right.'

            # send the model's response to the Discord channel
            await message.channel.send(response)


def generate_message(message):
    model_engine = "text-davinci-003"
    prompt = f"${message.content}"
    completions = openai.Completion.create(engine=model_engine,
                                           prompt=prompt,
                                           max_tokens=1024,
                                           stop=None,
                                           temperature=0.9)
    message = completions.choices[0].text
    return message


def main():
    client = DiscordBotClient()
    client.run(DISCORD_TOKEN)


if __name__ == '__main__':
    main()
