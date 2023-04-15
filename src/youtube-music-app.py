import argparse
import requests
import json

ytm_endpoint = "http://localhost:9863/query"


fonts = {
    "pause": "",
    "play": "",
    "like": "",
    "dislike": "󰔑",
    "progress": ''
}


def get_request():
    return requests.get(ytm_endpoint).json()

def song_name():
    response = get_request()
    track = response['track']
    return f"{track['author']} - {track['title']}"

def song_status():
    response = get_request()
    player = response['player']
    if player['isPaused']:
        return fonts["pause"]
    else:
        return fonts["play"]

def song_percentage(char_len=12):
    percentage = get_request()['player']['statePercent']
    char_len -= 1
    to_print = int(percentage*char_len)
    return '[' + fonts['progress']*to_print + '.'*(char_len - to_print - 1) + ']'
    #return f"[{''.join('
    #return f"[{''.join('' if i < percentage*char_len else '.' for i in range(0, char_len+1))}]"

def is_song_liked():
    status = ['INDIFFERENT', 'LIKE', 'DISLIKE']
    song_liked = get_request()['player']['likeStatus']
    if song_liked == status[1]:
        return fonts["like"] + " "
    elif song_liked == status[2]:
        return fonts["dislike"] + " "
    else:
        return ""

def print_status(char_len=12):
    print(f"{song_status()} {song_name()} {is_song_liked()}{song_percentage(char_len)}")


def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', help="Print get command")
    parser.add_argument('--progress-bar', type=int, default=12, help='Size of the progress bar')
    parser.add_argument('--no-nerd-font', action='store_true', help='Disable nerd fonts')
    return parser.parse_args()

def main():

    args = parser()

    if args.no_nerd_font:
        global fonts
        fonts = {
            "pause": "[PAUSE]",
            "play": "[PLAYING]",
            "like": "[LIKED]",
            "dislike": "[DISLIKED]",
            "progress": '='
        }

    if args.debug:
        print(get_request())
    else:
        print_status(args.progress_bar)

if __name__=="__main__":
    main()
