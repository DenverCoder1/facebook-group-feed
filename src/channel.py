from abc import ABCMeta, abstractmethod
from typing import Any, Mapping

import nextcord

from utils import trim_text


class Channel(metaclass=ABCMeta):
    """Channel class"""

    @abstractmethod
    def send(self, message: Mapping[str, Any]) -> None:
        """Send a message to the Discord webhook

        Args:
            message: The message to send (as returned by facebook_scraper.get_posts)
        """
        ...


class DiscordWebhookChannel(Channel):
    """Discord webhook channel"""

    def __init__(self, webhook_url: str):
        """Initialize the channel

        Args:
            webhook_url: The webhook url
        """
        self.webhook_url = webhook_url
        assert webhook_url, "You must set the WEBHOOK_URL environment variable to send messages"

    def send(self, message: Mapping[str, Any]) -> None:
        """Send a message to the Discord webhook

        Args:
            message: The message to send (as returned by facebook_scraper.get_posts)
        """
        webhook = nextcord.SyncWebhook.from_url(self.webhook_url)
        title = "New Post in Group"
        if "header" in message and isinstance(message["header"], str):
            title = message["header"].replace("\u200f", " · ")
        elif "username" in message:
            title = str(message["username"])
        post_url = message["post_url"] if "post_url" in message else None
        description = trim_text(message["post_text"], 1024) if "post_text" in message else ""
        description += f"\n\n[View Post]({post_url})" if post_url else ""
        timestamp = message["time"] if "time" in message else None
        embed = nextcord.Embed(
            title=title,
            description=description,
            url=post_url,
            color=nextcord.Color.green(),
            timestamp=timestamp,
        )
        if "images_lowquality" in message and len(message["images_lowquality"]) > 0:
            embed.set_image(url=message["images_lowquality"][0])
        webhook.send(embed=embed)
