import requests
import websocket
import json


EVENTSUB_WS_URL = "wss://eventsub.wss.twitch.tv/ws"
SUB_URL = "https://api.twitch.tv/helix/eventsub/subscriptions"


def create_subscription(session_id: str,
                        client_id: str,
                        user_access_token: str,
                        broadcaster_user_id: str,
                        reward_id: str):
    print("creating subscription...")

    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {user_access_token}",
        "Content-Type": "application/json",
    }
    
    body = {
        "type": "channel.channel_points_custom_reward_redemption.add",
        "version": "1",
        "condition": {
            "broadcaster_user_id": broadcaster_user_id,
            "reward_id": reward_id
        },
        "transport": {
            "method": "websocket",
            "session_id": session_id,
        },
    }

    req = requests.post(SUB_URL, headers=headers, json=body, timeout=15)
    print("subscription status: ", req.status_code)
    print(req.text)
    req.raise_for_status()

    print("subscription created")


def create_connection(client_id: str, 
                      user_access_token: str,
                      broadcaster_user_id: str, 
                      reward_id: str, tts_queue):
    ws = websocket.create_connection(EVENTSUB_WS_URL, timeout=30)
    ws.settimeout(30)
    print("WebSocket connection established.")

    subscribed = False

    while True:
        try:
            print("Waiting for WebSocket message...")
            raw = ws.recv()
            print("Received:", raw)
        except websocket.WebSocketTimeoutException:
            print("Timed out waiting for websocket message.")
            continue
        except Exception as e:
            print("[WS ERROR]", e)
            break

        msg = json.loads(raw)

        mata = msg.get("metadata", {})
        payload = msg.get("payload", {})
        message_type = mata.get("message_type")

        print("message type: ", message_type)
        print(json.dumps(msg, ensure_ascii=False, indent=2))

        if message_type == "session_welcome":
            on_welcome(payload, subscribed,
                       client_id, user_access_token,
                       broadcaster_user_id, reward_id)
        
        elif message_type == "notification":
            on_notification(payload, tts_queue)

        elif message_type == "session_keepalive":
            pass

        elif message_type == "session_reconnect":
            print("[WS] Reconnect requested.")
            on_reconnect(payload, ws, subscribed)
        
        elif message_type == "revocation":
            print("Subscription revoked: ", payload)
            break

        else:
            print("[WS] Unknown message: ", message_type)
    
    print("[WS] Connection end.")


def on_welcome(payload, subscribed: bool, 
               client_id: str, user_access_token: str,
               broadcaster_user_id: str, reward_id: str):
    session = payload["session"]
    session_id = session["id"]
    print("Session ID: ", session_id)

    if not subscribed:
        create_subscription(session_id, client_id,
                            user_access_token, broadcaster_user_id, reward_id)
        subscribed = True


def on_notification(payload, tts_queue):
    event = payload.get("event", {})
    user_input = event.get("user_input")
    reward = event.get("reward", {})
    reward_title = reward.get("title")

    print("=== redemption detected ===")
    print("user_input: ", user_input)
    print("reward_title: ", reward_title)

    tts_queue.put(user_input)


def on_reconnect(payload, ws: websocket.WebSocket, subscribed: bool):
    reconnect_url = payload.get("url")
    print("Reconnecting to: ", reconnect_url)

    ws.close()
    ws = websocket.create_connection(reconnect_url, timeout=30)
    subscribed = True # Assume subscription is still valid after reconnect