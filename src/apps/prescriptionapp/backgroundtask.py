import time
import requests
import aiohttp
import asyncio


async def notify_push_medicine(token, title, message, session, extra=None, categoryId='pharmacyrequest', channelId='pharmacyrequest'):
    data = {
        'to': token,
        'title': title,
        'body': message,
        'data': dict(),
        "sound": 'default',
        'categoryId': categoryId,
        'channelId': channelId,
    }
    url = 'https://exp.host/--/api/v2/push/send'
    async with session.post(url, json=data) as res:
        result = res.status
        return result


async def notify_users(title, notification_ids,pres_id):
    try:
        actions = []
        async with aiohttp.ClientSession() as session:
            for notification in notification_ids:
                print(notification)
                actions.append(asyncio.ensure_future(notify_push_medicine(
                    notification, title,
                    str(pres_id), session)))
                
            results = await asyncio.gather(*actions)
            print(results,"results here")
        return "done"
    except Exception as e:
        print(e)
        
# async def notify_all_medicine_users():
#     try:
#         actions = []
#         async with aiohttp.ClientSession() as session:
#             pass
            

        




    
    




