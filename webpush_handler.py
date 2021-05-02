from pywebpush import webpush, WebPushException
import json
from main import app

def trigger_push_notification(push_subscription, title, body, column):
    try:
        response = webpush(
            subscription_info=push_subscription['subscription_json'],
            data=json.dumps({"title" : title, "body" : body}),
            vapid_private_key=app.config["VAPID_PRIVATE_KEY"],
            vapid_claims={
                "sub" : "mailto:{}".format(app.config["VAPID_CLAIM_EMAIL"])
            },
            ttl=60*60*24*3
        )
        return response.ok
    except WebPushException as exception:
        if exception.response and exception.response.json():
            extra = exception.response.json()
            print("Remote service replied with a {}:{}, {}",
                  extra.code,
                  extra.errno,
                  extra.message
                  )
            if(extra.code == 404 or extra.code == 410 or extra.errno == 404 or extra.errorno == 410):
                subscription_delete = push_subscription['subscription_json']
                column.delete_one({'endpoint' : subscription_delete['endpoint']})
                print("Deleted "  , subscription_delete)
        return False


def trigger_push_notifications_for_subscriptions(subscriptions, title, body, column):
    return [trigger_push_notification(subscription, title, body, column)
            for subscription in subscriptions]
