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
            }
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
                  
        return False


def trigger_push_notifications_for_subscriptions(subscriptions, title, body, column):
    return [trigger_push_notification(subscription, title, body, column)
            for subscription in subscriptions]
