import os
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

        self._help_message = f"""
### Matrix Youtube-DL Bot
Commands:
- {self._prefix}help : Help command, displays this message
- {self._prefix}dl <youtube url>: Download command, download and upload a youtube video
[Source Code](https://github.com/ib4519894/matrix-youtube-dl-bot)
"""
    
    def _add_callbacks(self) -> None:
        @self.listener.on_message_event
        async def message(room: Any, event: Any) -> None: #room and event are objects from the nio module
            """Runs relevant callbacks on message events, calls help() callback if none of the messages "handled" the message and the message had the right prefix."""
            match = botlib.MessageMatch(room, event, self, self._prefix)
            if not match.prefix():
                return
            callbacks = [ #Add callbacks here
            download
            ]
            handled = False
            for callback in callbacks:
                if (await callback(room, event)):
                    handled = True
            if handled:
                return
            await help(room, event)
        
        async def help(room: Any, event: Any) -> None:
            await self.api.send_markdown_message(room.room_id, message=self._help_message)
        
        async def incorrect_syntax(room_id: str) -> None:
            await self.api.send_markdown_message(room_id, message=f"Incorrect Syntax </br>{self._help_message}")
        
        async def download(room: Any, event: Any) -> bool:
            match = botlib.MessageMatch(room, event, self, self._prefix)
            if not (match.command("dl") or match.command("download")):
                return False

            if len(match.args()) != 1:
                await incorrect_syntax(room.room_id)
                return True
            
            parsed = src.parse(match.args()[0])
            if not parsed:
                await incorrect_syntax(room.room_id)
                return True
            
            path = f'./{parsed[-11:]}.mp4'
            self._youtube_dl_options['outtmpl'] = path

            await self.api.send_text_message(room.room_id, message=f"Downloading {path}...")
            with youtube_dl.YoutubeDL(self._youtube_dl_options) as ydl:
                ydl.download([parsed])
            
            await src.upload(self, room.room_id, path)

            os.system(f"rm {path}")
