import discord
import requests

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True

client = discord.Client(intents=intents)

api_keys = {}  # Temporary storage for API keys

@client.event
async def on_ready():
    print('Bot is ready.')

@client.event
async def on_message(message):
    if message.content.startswith('/start'):
        await message.channel.send("Please provide your X-API-Key:")
        x_api_key = await client.wait_for('message', check=lambda m: m.author == message.author)
        await message.channel.send("Please provide your X-Org-Key:")
        x_org_key = await client.wait_for('message', check=lambda m: m.author == message.author)
        api_keys[message.author.id] = {
            'x_api_key': x_api_key.content,
            'x_org_key': x_org_key.content
        }
        await message.channel.send("API keys saved for this session.")

    elif message.content.startswith('/image'):
        await message.channel.send("Enter Image description:")
        user_input = await client.wait_for('message', check=lambda m: m.author == message.author)

        if message.author.id not in api_keys:
            await message.channel.send("Please use /start command to provide API keys first.")
            return

        # Retrieve the user's API keys from temporary storage
        x_api_key = api_keys[message.author.id]['x_api_key']
        x_org_key = api_keys[message.author.id]['x_org_key']

        await message.channel.send("Generating the image...")

        # Make a request to the image API using the provided inputs and the retrieved API keys
        api_url = 'https://api.worqhat.com/api/ai/images/generate/v2'
        headers = {
            'X-API-Key': x_api_key,
            'X-Org-Key': x_org_key,
            'Content-Type': "application/json"
        }
        payload = {
            'prompt': [user_input.content]
        }
        response = requests.post(api_url, headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                content_link = data['content']
                await message.channel.send("Here is your generated image:")
                await message.channel.send(content_link)
            else:
                await message.channel.send("Image generation failed.")
        else:
            await message.channel.send("An error occurred while making the image API request.")

    elif message.content.startswith('/text'):
        await message.channel.send("Enter Text:")
        user_input = await client.wait_for('message', check=lambda m: m.author == message.author)

        if message.author.id not in api_keys:
            await message.channel.send("Please use /start command to provide API keys first.")
            return

        # Retrieve the user's API keys from temporary storage
        x_api_key = api_keys[message.author.id]['x_api_key']
        x_org_key = api_keys[message.author.id]['x_org_key']

        await message.channel.send("Processing the text...")

        # Make a request to the text API using the provided inputs and the retrieved API keys
        api_url = 'https://api.worqhat.com/api/ai/content/v2'
        headers = {
            'X-API-Key': x_api_key,
            'X-Org-Key': x_org_key,
            'Content-Type': "application/json"
        }
        payload = {
            'question': user_input.content
        }
        response = requests.post(api_url, headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                content = data['content']
                await message.channel.send("Here is the generated text:")
                await message.channel.send(content)
            else:
                await message.channel.send("Text processing failed.")
        else:
            await message.channel.send("An error occurred while making the text API request.")

TOKEN = os.getenv('TOKEN')
client.run(TOKEN)
