import os
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from github import Github

# Set your Slack and GitHub tokens as environment variables or configure them here.
slack_token = os.environ["SLACK_TOKEN"]
github_token = os.environ["GITHUB_TOKEN"]
slack_channel_id = "#test"  # Replace with the desired Slack channel ID.

# Initialize the Slack and GitHub clients
slack_client = WebClient(token=slack_token)
github_client = Github(github_token)

# Initialize the Slack Event Adapter for handling slash commands
slack_signing_secret = os.environ["SLACK_SIGNING_SECRET"]
slack_events_adapter = SlackEventAdapter(slack_signing_secret, "/slack/events")

# Function to onboard a new user
def onboard_user(username):
    # Implement your logic here for onboarding a user in GitHub.
    # You can add them to the GitHub organization, set permissions, etc.
    # Then, send a Slack message to notify the user about onboarding.
    slack_client.chat_postMessage(
        channel=slack_channel_id,
        text=f"Welcome {username} to our GitHub organization! You are onboarded."
    )

# Function to offboard a user
def offboard_user(username):
    # Implement your logic here for offboarding a user in GitHub.
    # This could involve removing them from the GitHub organization, revoking access, etc.
    # Then, send a Slack message to notify the user about offboarding.
    slack_client.chat_postMessage(
        channel=slack_channel_id,
        text=f"Goodbye {username}. You are offboarded from our GitHub organization."
    )

# Event listener for slash commands
@slack_events_adapter.on("slash_command")
def handle_slash_command(event_data):
    command = event_data["command"]
    user_id = event_data["user_id"]
    text = event_data["text"]

    if command == "/onboard":
        # Extract the GitHub username from the slash command text.
        # Assuming the format is: /onboard <github_username>
        args = text.split()
        if len(args) != 1:
            slack_client.chat_postMessage(
                channel=slack_channel_id,
                text="Invalid usage. Please provide the GitHub username."
            )
        else:
            username = args[0]
            onboard_user(username)

    elif command == "/offboard":
        # Extract the GitHub username from the slash command text.
        # Assuming the format is: /offboard <github_username>
        args = text.split()
        if len(args) != 1:
            slack_client.chat_postMessage(
                channel=slack_channel_id,
                text="Invalid usage. Please provide the GitHub username."
            )
        else:
            username = args[0]
            offboard_user(username)

if __name__ == "__main__":
    slack_client.chat_postMessage(channel=slack_channel_id, text="Hello! I'm your GitHub integration bot.")
    slack_events_adapter.start(host="0.0.0.0", port=3000)
