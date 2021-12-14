import time
import requests
import aiohttp
import asyncio
from typing import Optional
from .models import Cart,DunzoOrder

async def notify_push_medicine(token:str, title:str, message:str,session, extra:Optional[dict]={},sound:Optional[str]="default",categoryId:Optional[str]='pharmacyrequest', channelId:Optional[int]='pharmacyrequest'):
    data = {
        'to': token,
        'title': title,
        'body': message,
        'data': extra,
        "sound": sound,
        'categoryId': categoryId,
        'channelId': channelId,
    }
    url = 'https://exp.host/--/api/v2/push/send'
    async with session.post(url, json=data) as res:
        result = res.status
        return result


async def notify_users(title, notification_ids, pres_id):
    try:
        actions = []
        async with aiohttp.ClientSession() as session:
            for notification in notification_ids:
                print(notification)
                actions.append(asyncio.ensure_future(notify_push_medicine(
                    notification, title,
                    str(pres_id), session)))
            results = await asyncio.gather(*actions)
            print(results, "results here")
        return "done"
    except Exception as e:
        print(e)
        
async def notify(title, message,extra,notification_ids):
    try:
        actions = []
        async with aiohttp.ClientSession() as session:
            for notification in notification_ids:
                print(notification)
                actions.append(asyncio.ensure_future(notify_push_medicine(
                    notification, title,
                    message, session)))

            results = await asyncio.gather(*actions)
            print(results, "results here")
        return "done"
    except Exception as e:
        print(e)
        
async def notify_medicalstore(title, notification_ids, pres_id):
    try:
        actions = []
        loop = asyncio.new_event_loop()

        async with aiohttp.ClientSession() as session:
            for notification in notification_ids:
                print(notification)
                actions.append(asyncio.ensure_future(notify_push_medicine(
                    notification, title,
                    str(pres_id), session)))
            all_groups = await asyncio.gather(*actions)
            results = loop.run_until_complete(all_groups) 
            print(results, "results here")
            loop.close()
        return "done"
    except Exception as e:
        loop.close()
        print(e)
        
async def notify_cancel_order(cart,notification_ids,user_ids):
    try:
        actions = []
        loop = asyncio.new_event_loop()
        async with aiohttp.ClientSession() as session:
            for notification in notification_ids:
                print(notification)
                actions.append(asyncio.ensure_future(notify_push_medicine(
                    notification, 'orderalert', "you have a incoming order accept it within five mins", session,
                    {"cartid":cart})))
            all_groups = await asyncio.gather(*actions)
            results = loop.run_until_complete(all_groups)
            
        await asyncio.sleep(300)
        print("im back")
        get_cart = await Cart.get(id=cart)
        if get_cart.order_status != "Accepted":
            get_cart.order_status = "TimeOutCancelled"
            await get_cart.save()
            user_actions = []
            title = "your orders was cancelled by the medical store try different shops sorry for the inconvenience"
            async with aiohttp.ClientSession() as session:
                for notification in user_ids:
                    user_actions.append(asyncio.ensure_future(notify_push_medicine(
                        notification, 'medical alert', title,
                        session,{"cartid": cart},)))
                all_groups = await asyncio.gather(*actions)
                results = loop.run_until_complete(all_groups)
        loop.close()
        print(results, "results here")
        print(results, "results here")
        return "done"
    except Exception as e:
        loop.close()
        print(e)
from src.apps.razorpay.endpoints import client


async def notify_dunzo_order(cart,dunzo,notification_ids, user_ids):
    try:
        actions = []
        loop = asyncio.new_event_loop()
        async with aiohttp.ClientSession() as session:
            for notification in notification_ids:
                print(notification)
                actions.append(asyncio.ensure_future(notify_push_medicine(
                    notification, 'orderalert', "you have a incoming order accept it within five mins", session,
                    {"cartid":cart})))
            all_groups = await asyncio.gather(*actions)
            results = loop.run_until_complete(all_groups)
        await asyncio.sleep(200)
        get_cart = await Cart.get(id=cart)
        if get_cart.order_status != "Accepted":
            get_cart.order_status = "TimeOutCancelled"
            await get_cart.save()
            user_actions = []
            title = "your orders was cancelled by the medical store try different shops sorry for the inconvenience and money will be refunded shortly within 24 hrs"
            async with aiohttp.ClientSession() as session:
                for notification in user_ids:
                    print(notification)
                    user_actions.append(asyncio.ensure_future(notify_push_medicine(
                        notification, 'medical alert', title,
                        session,{"cartid": cart},)))
                all_groups = await asyncio.gather(*actions)
                results = loop.run_until_complete(all_groups)
            # p = await DunzoOrder.get(id=dunzo)
            # try:
            #     refund = client.payment.refund(
            #         params['razorpay_payment_id'], round(p.razor_price))
            #     p.is_refunded = True
            #     p.is_cancelled = True
            #     p.refund_id = refund['id']
            #     p.save()
            #     return "success refunded"
            # except Exception as e:
            #     print(e)
            #     # p.is_cancelled = True
            #     # p.save()
            #     return "error something went wrong"
        print(results, "results here")
        loop.close()
        return "done"
    except Exception as e:
        loop.close()
        print(e)
