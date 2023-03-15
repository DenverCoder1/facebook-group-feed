# facebook-group-feed

Send new messages from public Facebook groups to a Discord channel.

To send messages to a different source, subclass the `Channel` abstract base class (ABC) in `channel.py` and implement the `send()` method. An example structure of a post can be found in [`structure.md`](structure.md).

## Installation of dependencies

Optionally, create a virtual environment and activate it to avoid installing dependencies globally.

```bash
virtualenv .venv

# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate.bat
```

Install the dependencies.

```bash
pip install -r requirements.txt
```

## Usage

```bash
cd src
python -m main
```

The exact command to run depends on your Python installation. If you have multiple versions of Python installed, you may need to run `python3` instead of `python`.

## Configuration

The environment variables `DISCORD_WEBHOOK_URL` and `FACEBOOK_GROUP_IDS` must be set.

The Discord webhook URL can be obtained by creating a webhook in the Discord channel you want to send messages to (1) Right-click on the channel and select "Edit channel", (2) In the "Integrations" panel, select "Webhooks" then "New Webhook", (3) Give the webhook a name and press "Copy Webhook URL" to obtain the URL for sending to the webhook.

The Facebook group ID can be obtained by looking at the URL of the group. For example, the group ID for https://www.facebook.com/groups/1234567890/ is `1234567890`. The group ID may also be a string representing the group name if it appears in the URL.

The variable `SENT_POSTS_FILENAME` can optionally be set to change the filename of the file that stores the IDs of posts that have already been sent. The default is `sent_posts.txt`.
