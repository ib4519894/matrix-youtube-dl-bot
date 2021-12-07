import sys
import simplematrixbotlib as botlib
import src

def main() -> None:
    creds = botlib.Creds(homeserver=sys.argv[1], username=sys.argv[2], password=sys.argv[3])
    bot = src.Bot(creds)
    bot.run()

if __name__ == '__main__':
    main()