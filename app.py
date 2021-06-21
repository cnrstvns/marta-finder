from dotenv import load_dotenv
import requests
import discord
import boto3
import os

# Load ENV Variables
load_dotenv()

# Connect to APIs
client = discord.Client()
rekog = boto3.client(
    "rekognition",
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"), 
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name = os.getenv("AWS_REGION")
)

# Handle ready event
@client.event
async def on_ready():
    print('Connected to Discord')

# Handle message event
@client.event
async def on_message(message):
    if message.attachments:
        for attachment in message.attachments:
            try:
                image = requests.get(attachment.url)
                response = rekog.detect_labels(Image = {"Bytes": image.content })
                if 'Cat' in [item['Name'] for item in response['Labels']]:
                    await message.delete()
                    await message.channel.send('Detected a cat')
            except Exception as e:
                pass

client.run(os.getenv('TOKEN'))
