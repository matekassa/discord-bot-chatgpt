import discord
import openai
from decouple import config

DISCORD_TOKEN = config('DISCORD_TOKEN')
openai.organization = config('OPENAI_ORG')
openai.api_key = config('OPENAI_API_KEY')


class DiscordBotClient(discord.Client):

    def __init__(self):
        # Adding intents module to prevent intents error in __init__ method in newer versions of Discord.py
        intents = discord.Intents.default()  # Select all the intents in your bot settings as it's easier
        intents.message_content = True
        super().__init__(intents=intents)
        self.api_endpoint = openai.api_key

    async def on_ready(self):
        # Print out information when the bot wakes up
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        # Ignore the message if it comes from the bot itself
        if message.author.id == self.user.id:
            return
        # While the bot is waiting on a response from the model, set its status as typing for user-friendliness
        async with message.channel.typing():
            response = generate_message(message)
            # We may get ill-formed response if the model hasn't fully loaded or has timed out
            if not response:
                if 'error' in response:
                    response = '`Error: {}`'.format(response['error'])
                else:
                    response = 'Hmm... something is not right.'
            # Send the model's response to the Discord channel
            await message.channel.send(response)


def generate_message(message):
    """
    The function returns the message that is going to be sent by the bot.
    :param message: message from the discord client
    :return: ai generated bot answer
    """
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
