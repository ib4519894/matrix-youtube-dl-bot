import simplematrixbotlib as botlib
import youtube_dl
import src
from typing import Any
from simplematrixbotlib import Creds, Config

class Bot(botlib.Bot):
    def __init__(self, creds: Creds, config: Config=None, youtube_dl_options: dict={}) -> None:
        super().__init__(creds, config)
        self._youtube_dl_options = youtube_dl_options
        self._add_callbacks()
        self._prefix = "y!"
    
    def _add_callbacks(self) -> None:

        @self.listener.on_message_event
        async def message(room: Any, event: Any) -> None: #room and event are objects from the nio module
            """Runs relevant callbacks on message events, calls help() callback if none of the messages "handled" the message and the message had the right prefix."""
            match = botlib.MessageMatch(room, event, self, self._prefix)
            if not match.prefix():
                return
            callbacks = [ #Add callbacks here
            ]
            handled = False
            for callback in callbacks:
                if (await callback(room, event)):
                    handled = True
            if handled:
                return
            await help(room, event)
        
        async def help(room: Any, event: Any) -> None:
            message = f"""
### Matrix Youtube-DL Bot
Commands:
- {self._prefix}help : Help command, displays this message
- {self._prefix}dl <youtube url>: Download command, download and upload a youtube video
[Source Code](https://github.com/ib4519894/matrix-youtube-dl-bot)
"""
            await self.api.send_markdown_message(room.room_id, message=message)