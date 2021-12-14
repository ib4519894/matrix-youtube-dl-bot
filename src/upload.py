import os
from nio import UploadResponse
import simplematrixbotlib as botlib
import mimetypes
import aiofiles

async def upload(bot: botlib.Bot, room_id: str, path: str) -> None:
    mime_type = mimetypes.guess_type(path)[0]

    with open(path, 'rb') as file:
        file_stat = await aiofiles.os.stat(path)

        async with aiofiles.open(path, "r+b") as file:
            resp, maybe_keys = await bot.async_client.upload(
                file,
                content_type=mime_type,
                filename=os.path.basename(path),
                filesize=file_stat.st_size)

        if isinstance(resp, UploadResponse):
            pass  #Successful upload
        else:
            print(f"Failed Upload Response: {resp}")

        content = {
            "body": os.path.basename(path),
            "info": {
                "size": file_stat.st_size,
                "mimetype": mime_type,
            },
            "msgtype": "m.file",
            "url": resp.content_uri
        }

        server = (resp.content_uri.split("/")[2])
        media_id = (resp.content_uri.split("/")[3])

        try:
            await bot.async_client.room_send(room_id,
                                              message_type="m.room.message",
                                              content=content)
            await bot.api.send_text_message(room_id, message=f"https://{server}/_matrix/media/v3/download/{server}/{media_id}")
        except:
            print(f"Failed to send file {path}")
