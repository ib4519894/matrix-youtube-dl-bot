from typing import List

def parse(input_text: str) -> List[str]:
    urls = []
    for part in input_text.split():
        match = re.findall(r'(https?://)?(www\.)?''(youtube|youtu|youtube-nocookie)\.(com|be)/''(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})', part)
        if list(match):
            urls.append(f"https://www.youtube.com/watch?v={match[0][5]}")
    return urls