import discord
import asyncio

from threading import Thread
from csgo.updates import get_latest_update, read_latest_title, write_latest_title
from logs.logger import logger

client = discord.Client()
test_channel = None
global title_in_memory
title_in_memory = read_latest_title()


@client.event
async def on_ready():
    logger.info('Bot logged in as {0.user}'.format(client))
    channel = client.get_channel(700066521317113886)
    logger.info("Connected to %s", channel)
    while True:
        await check_csgo_rss(channel)


async def send_message(message_text, channel):
    csgo_update_sections = message_text.split('\n\n')
    for section in csgo_update_sections:
        await channel.send('```' + section + '```')


async def check_csgo_rss(channel):
    global title_in_memory
    await asyncio.sleep(120)
    logger.info("Checking CSGO blog for update...")
    latest_title, update_text = get_latest_update()
    logger.info(latest_title)
    if title_in_memory != latest_title:
        logger.info(
            "New CSGO update found titled \"%s\". Sending message to %s...", latest_title, channel)
        await send_message(update_text, channel)
        write_latest_title(latest_title)
        title_in_memory = latest_title
    else:
        logger.info("No new update found.")

client.run('NzA0MzY1MDM5MDAzNjMxNzY2.XqcFlg.2cblpsi9QoF_4b5ApM473tVKcpg')
