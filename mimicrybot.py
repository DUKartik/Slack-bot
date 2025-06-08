from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
import os
# from dotenv import load_dotenv

load_dotenv()

# initialize the App with bot token
app= App(token=os.environ["SLACK_BOT_TOKEN"])


# respond when user @ mention chatbot
@app.event("app_mention") # decorater

def handle_app_mention(body,say,logger):
    event=body.get("event",{})
    # channel_id=event.get('channel')
    user_id=event.get("user")
    text=event.get("text")
    if not text:
        return 
    
    cleaned_text = ' '.join(text.split()[1:])

    say(f"<@{user_id}> you said : {cleaned_text}")



# Respond to any message event
@app.event("message")
def handle_message_events(body, say, logger):
    event = body.get("event", {})
    
    # Avoid reacting to bot's own messages
    if event.get("subtype") == "bot_message":
        return

    user = event.get("user")
    text = event.get("text")

    if not user or not text:
        return

    logger.info(f"Received message from {user}: {text}")
    say(f"<@{user}> you said: {text}")




if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()