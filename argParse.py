import argparse, sys

def ParseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user", help="twitch user name", required=True)
    parser.add_argument("-m", "--month", help="Month to examine", required=True)
    parser.add_argument("-y", "--year", help="Year to examine", required=True)
    parser.add_argument('-his', help="Full history from provided month/year to start", action='store_true')
    parser.add_argument('-pl', help="Parse Only", action='store_true')
    parser.add_argument('-dc', help="Daily Count Only", action='store_true')
    args = parser.parse_args()

    return args