import sys
import simplematrixbotlib as botlib
import src

YOUTUBE_DL_OPTS = {
    #'max_filesize' : 50
}

def main() -> None:
    creds = botlib.Creds(homeserver=sys.argv[1], username=sys.argv[2], password=sys.argv[3])
    bot = src.Bot(creds, youtube_dl_options=YOUTUBE_DL_OPTS)
    bot.run()

if __name__ == '__main__':
    main()