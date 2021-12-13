from typing import List
import re

def parse(input_text: str) -> str:
    for part in input_text.split():
        match = re.findall(r'(https?://)?(www\.)?''(youtube|youtu|youtube-nocookie)\.(com|be)/''(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})', part)
        if list(match):
            return f"https://www.youtube.com/watch?v={match[0][5]}"
