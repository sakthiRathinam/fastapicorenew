import time
import requests
import aiohttp
import asyncio


async def send_sound_message(token, title, message, extra=None, categoryId=None, channelId=None):
    try:
        data = {
            'to': token,
            'title': title,
            'body': message,
            'extra': extra,
            "sound": 'default',
            'categoryId': categoryId,
            'channelId': channelId,
        }
        r = requests.post('https://exp.host/--/api/v2/push/send', json=data)
    except:
        pass


async def send_order_message(token, title, message, extra=None, categoryId=None, channelId=None):
    try:
        data = {
            'to': token,
            'title': title,
            'body': message,
            'extra': extra,
            "sound": 'default',
            'categoryId': categoryId,
            'channelId': channelId,
        }
        r = requests.post('https://exp.host/--/api/v2/push/send', json=data)
    except:
        pass


async def send_prescription(token, title, message, data):
    try:
        data = {
            'to': token,
            'title': title,
            'body': message,
            "sound": 'default',
            'categoryId': 'prescription',
            'channelId': 'aa',
            'data': data
        }
        r = requests.post('https://exp.host/--/api/v2/push/send', json=data)
    except:
        pass



