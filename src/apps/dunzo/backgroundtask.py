import time
import requests
import aiohttp
import asyncio
async def notify_push(token, title, message, data, session, extra=None, categoryId='pharmacyrequest', channelId='pharmacyrequest'):
    data = {
        'to': token,
        'title': title,
        'body': message,
        'extra': extra,
        'data': data,
        "sound": 'default',
        'categoryId': categoryId,
        'channelId': channelId,
    }
    url = 'https://exp.host/--/api/v2/push/send'
    async with session.post(url, json=data) as res:
        result = res.status
        return result


async def notify_all_medicals(order, notification_ids):
    try:
        starting_time = time.time()
        actions = []
        title = "Order Alert"
        message = "Kindly Accept the order if you have all the medicines"
        data = {
            "orderid": order
        }
        async with aiohttp.ClientSession() as session:
            for notification in notification_ids:
                if len(notification) > 1:
                    actions.append(asyncio.ensure_future(notify_push(
                        notification, title, message, data, session)))
            results = await asyncio.gather(*actions)
        return total_time
    except Exception as e:
        print(e)
