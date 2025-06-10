from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
import os
from slack_sdk.errors import SlackApiError

# from dotenv import load_dotenv
load_dotenv()
SLACK_BOT_TOKEN=os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN=os.environ["SLACK_APP_TOKEN"]


# initialize the App with bot token
app= App(token=SLACK_BOT_TOKEN)

@app.command("/message-count")
def handle_message_count(ack, respond, command, client):
    ack()

    channel_id = command["channel_id"]
    user_id = command["user_id"]

    try:
        # Call conversations.history to fetch messages
        result = client.conversations_history(channel=channel_id, limit=1000)
        messages = result["messages"]

        message_count = len(messages)

        respond(f"<@{user_id}> there are *{message_count}* messages in this channel (latest 1000).")

    except SlackApiError as e:
        respond(f"Failed to count messages: {e.response['error']}")


if __name__ == "__main__":
    handler = SocketModeHandler(app,SLACK_APP_TOKEN)
    handler.start()