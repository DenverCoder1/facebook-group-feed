import concurrent.futures
import os
import time
from datetime import datetime
from typing import Any, Callable, Iterable, Mapping

from dotenv import load_dotenv
from facebook_scraper import get_posts

import channel

load_dotenv()

FACEBOOK_GROUP_IDS: list[str] = os.getenv("FACEBOOK_GROUP_IDS", "").split(",")
SENT_POSTS_FILENAME: str = os.getenv("SENT_POSTS_FILENAME", "sent_posts.txt")

CHANNEL: channel.Channel = channel.DiscordWebhookChannel(os.getenv("WEBHOOK_URL", ""))


def process_posts_in_group(group: str | int, callback: Callable[[Mapping[str, Any]], None]) -> None:
    """Fetches posts from a group and calls the callback function for each post

    Args:
        group: The group id
    """
    for post in get_posts(group=group, pages=2, options={"comments": 0, "progress": True}):
        callback(post)


def get_sent_post_ids() -> set[str]:
    """Get the ids of the posts we've already sent

    Returns:
        A set of post ids
    """
    sent_posts = set()
    if not os.path.exists(SENT_POSTS_FILENAME):
        open(SENT_POSTS_FILENAME, "w+").close()
    with open(SENT_POSTS_FILENAME, "r") as f:
        for line in f:
            sent_posts.add(line.strip())
    return sent_posts


def write_sent_post_ids(sent_posts: set[str]) -> None:
    """Write the ids of the posts we've already sent

    Args:
        sent_posts: A set of post ids
    """
    with open(SENT_POSTS_FILENAME, "a") as f:
        for post_id in sent_posts:
            f.write(post_id + "\n")


def send_message(message: Mapping[str, Any]) -> None:
    """Send a message to the Discord webhook and write the post id to the sent posts file

    Args:
        message: The message to send (as returned by facebook_scraper.get_posts)
    """
    print("Sending message: " + message["post_url"])
    CHANNEL.send(message)
    write_sent_post_ids({message["post_id"]})


def send_test_message() -> None:
    """Send a test message to the Discord webhook"""
    send_message(
        {
            "post_id": "43284432493284792374",
            "post_text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec auctor, nisl eget ultricies lacinia, nunc nisl aliquam nunc, eget ultricies.",
            "images_lowquality": ["https://via.placeholder.com/640x360"],
            "post_url": "https://m.facebook.com/groups/groupname/permalink/5839808520835092/",
            "header": "Jonah Lawrence\u200fGroup Name",
            "time": datetime.now(),
            "timestamp": 1621234567,
            "username": "Jonah Lawrence",
        }
    )


def send_all_new_messages(groups: Iterable[str | int]) -> None:
    """Send all new messages from the given groups to the Discord webhook

    Args:
        groups: A list of group identifiers
    """
    sent_posts = get_sent_post_ids()

    def send_post_callback(post: Mapping[str, Any]) -> None:
        """Send a post to the Discord webhook if it's new"""
        # if the post is older than 5 hours, don't send it (compare unix timestamps)
        if post["timestamp"] < time.time() - 60 * 60 * 5:
            return
        # if the post is already sent, don't send it again
        if post["post_id"] in sent_posts:
            return
        # otherwise, send it
        send_message(post)

    # create a thread pool to process the groups in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for group in groups:
            executor.submit(process_posts_in_group, group, send_post_callback)


if __name__ == "__main__":
    print(f"Checking for new messages in groups: {', '.join(FACEBOOK_GROUP_IDS)}")
    while True:
        send_all_new_messages(FACEBOOK_GROUP_IDS)
        print("Checking again in 5 minutes...")
        time.sleep(60 * 5)  # sleep for 5 minutes before checking again
