import requests
import argParse
import os, sys, csv

# Gets the requested log. Returns the response request objet
def GetLog(user, month, year):
    url = "https://overrustlelogs.net/{} chatlog/{} {}/subscribers.txt".format(user, month, year)
    res = requests.get(url)
    return res

def ParseLog(log):
    subs = log.split("\n")[:-1]
    sub_count = len(subs)
    sub_prime = 0
    sub_t1 = 0
    sub_t2 = 0
    sub_t3 = 0
    sub_money = 0
    for line in subs:
        if " with Twitch Prime" in line:
            sub_money += 4.99
            sub_prime += 1
        elif " $4.99 " in line:
            sub_money += 4.99
            sub_t1 += 1
        elif " $9.99 " in line:
            sub_money += 9.99
            sub_t2 += 1
        elif " $24.99 " in line:
            sub_money += 24.99
            sub_t3 += 1
        elif "resubscribed while you were away" in line:
            num = int(line.split("twitchnotify:")[1].split()[0])
            subs[day]['sub_money'] += num*4.99
            subs[day]['sub_t1'] += num
        elif "just subscribed!" in line:
            subs[day]['sub_money'] += 4.99
            subs[day]['sub_t1'] += 1
        elif "months in a row!" in line:
            subs[day]['sub_money'] += 4.99
            subs[day]['sub_t1'] += 1

    print("{}\n${}\nPrime: {}\nT1: {}\nT2: {}\nT3: {}".format(sub_count, round(sub_money,2), sub_prime, sub_t1, sub_t2, sub_t3))

def CountDays(log):
    day_count = {}
    for line in log[:-1]:
        day = line[1:11]
        if not day in day_count:
            day_count[day] = 1
        else:
            day_count[day] += 1
    return 

'''
Used with MoreSubDetails.
Input is a subs object, which is a dictionay with dates as keys:
+++++++++++++++
ex:
{'2017-12-01': {
    'daily_subs': <number>,
    'sub_lines': [<list of chat logs for that day>]
}}
'''
def GetDailyCount(subs):
    for day in subs.keys():
        subs[day]['sub_prime'] = 0
        subs[day]['sub_t1'] = 0
        subs[day]['sub_t2'] = 0
        subs[day]['sub_t3'] = 0
        subs[day]['sub_money'] = 0
        for line in subs[day]['sub_lines']:
            if " with Twitch Prime" in line:
                subs[day]['sub_money'] += 4.99
                subs[day]['sub_prime'] += 1
            elif " $4.99 " in line:
                subs[day]['sub_money'] += 4.99
                subs[day]['sub_t1'] += 1
            elif " $9.99 " in line:
                subs[day]['sub_money'] += 9.99
                subs[day]['sub_t2'] += 1
            elif " $24.99 " in line:
                subs[day]['sub_money'] += 24.99
                subs[day]['sub_t3'] += 1
            elif "resubscribed while you were away" in line:
                num = int(line.split("twitchnotify:")[1].split()[0])
                subs[day]['sub_money'] += num*4.99
                subs[day]['sub_t1'] += num
            elif "just subscribed!" in line:
                subs[day]['sub_money'] += 4.99
                subs[day]['sub_t1'] += 1
            elif "months in a row!" in line:
                subs[day]['sub_money'] += 4.99
                subs[day]['sub_t1'] += 1

        subs[day]['sub_money'] = round(subs[day]['sub_money'], 2)
        del subs[day]['sub_lines']
    return subs

# Similar to CountDays, only it's used calculate each type of subs and money made from subs.
# Expects input in the format returned when doing a GetLog().text.split('\n')
def MoreSubDetails(log):
    day_count = {}
    for line in log[:-1]:
        day = line[1:11]
        if not day in day_count:
            day_count[day] = {}
            day_count[day]['daily_subs'] = 1
            day_count[day]['sub_lines'] = [line]
        else:
            day_count[day]['daily_subs'] += 1
            day_count[day]['sub_lines'].append(line)
    day_count = GetDailyCount(day_count)
    return day_count

def WriteSubDetails(subs, stream):
    if not os.path.exists("csv"):
        os.makedirs("csv")
    file_exists = os.path.isfile("csv/{}.csv".format(stream))
    with open('csv/{}.csv'.format(stream), 'a') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(('date', 'daily_subs', 'prime_subs', 't1_subs', 't2_subs', 't3_subs', 'sub_money'))
        for day in list(subs.keys())[::-1]:
            temp = subs[day]
            writer.writerow((day, temp['daily_subs'], temp['sub_prime'], temp['sub_t1'], temp['sub_t2'], temp['sub_t3'], temp['sub_money']))

def GetFullHistory(args):
    months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
    log = GetLog(args.user, args.month, args.year)
    month = months.index(args.month)
    year = args.year

    while log.status_code == 200:
        subs = MoreSubDetails(log.text.split('\n'))
        WriteSubDetails(subs, args.user)

        # Get next month
        month = month - 1
        if month < 0:
            month = 11
            year = str(int(year) - 1)

        # Get next file
        log = GetLog(args.user, months[month], year)

def main():
    args = argParse.ParseArgs()
    if args.pl:
        log = GetLog(args.user, args.month, args.year)
        ParseLog(log.text)
        sys.exit()
    if args.dc:
        log = GetLog(args.user, args.month, args.year)
        subs = MoreSubDetails(log.text.split('\n'))
        WriteSubDetails(subs, args.user)
        sys.exit()
    if args.his:
        GetFullHistory(args)
        sys.exit()
    log = GetLog(args.user, args.month, args.year)
    ParseLog(log.text)

if __name__ == "__main__":
    main()