from src.spotify import Playlist, Spotify
from src.yt import YoutubeMusic
import argparse

def main():
    # create a parser object
    parser = argparse.ArgumentParser(description = "A utility for spotify API -> Youtube Download conversion")
    
    # add argument
    parser.add_argument("op", nargs = 1, metavar = "operation", type = str,
        help = "The operation to perform: playlist - gets spotify playlist | youtube - gets youtube search")

    parser.add_argument("val", nargs = '*', metavar = "value", type = str,
        help = "Either the spotify playlist URI to download or a Youtube Music search query string (+ delimited)")
    
    # parse the arguments from standard input
    args = parser.parse_args()

    # create the ytm object
    ytm = YoutubeMusic()

    if (args.op[0] == "playlist"):
        if (len(args.val) < 1):raise ValueError("Too many arguments for playlist operation!")
        tracks = []
        sp = Spotify()
        playlist = sp.get_playlist(args.val[0])

        for i in range(playlist.count()):
            tracks.append(playlist.getTrack(i))
        ytm.pull_queue(tracks)
    elif (args.op[0] == "youtube"):
        ytm.pull_queue(args.val)
    else:raise ValueError("Invalid Operation:", args.op[0])

if __name__ == "__main__":
    main()