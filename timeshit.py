import argparse
from datetime import *
import os
import json
from prettytable import PrettyTable
import matplotlib.pyplot as plt
import re

date = ""

# check if target time is between start and end timestamps
def isIn(target, start, end):
    targetH = int(target[0]+target[1])
    targetM = int(target[2]+target[3])

    startH = int(start[0]+start[1])
    startM = int(start[2]+start[3])

    endH = int(end[0]+end[1])
    endM = int(end[2]+end[3])
    if (startH,startM) <= (targetH,targetM) <= (endH,endM):
        return True
    return False

# generate minute-wise (key,None) pair for 24 hours
def createDay():
    out = {}
    for hr in range(24):
        for mi in range(60):
            out.setdefault(str(hr).rjust(2, '0')+str(mi).rjust(2, '0'), None)
    return out

# add work & note between 2 timestamps
def add(timestamps, workType=None, note=None):
    print("Adding stuff")
    print("Begin: {} End: {}".format(timestamps[0],timestamps[1]))
    workType = input("Please specify work type ") if workType == "custom" else workType
    print("Work Type: {}".format(workType))

    data = {}
    with open("./files/"+date+".json", "r+") as f:
        data = json.load(f)
        f.truncate(0)
    
    for each in data.keys():
        if isIn(each, timestamps[0], timestamps[1]):
            data[each] = {"workType": workType, "note": note}
    with open("./files/"+date+".json", "r+") as f:
        json.dump(data, f)  
    

# wipe data between 2 timestamps 
def remove(timestamps):
    print("Removing stuff")
    print("Begin: {} End: {}".format(timestamps[0],timestamps[1]))

    data = {}
    with open("./files/"+date+".json", "r+") as f:
        data = json.load(f)
        f.truncate(0)
    
    for each in data.keys():
        if isIn(each, timestamps[0], timestamps[1]):
            data[each] = None
    with open("./files/"+date+".json", "r+") as f:
        json.dump(data, f) 

# view whole day info in table/pie format
def view():
    print("Viewing date: "+date+"'s activity")
    data = {}
    with open("./files/"+date+".json", "r+") as f:
        data = json.load(f)
    #
    display = True
    hr = 0
    pivot = (None,None)
    info = {}
    for each in data.keys():
        if pivot[1] != data[each] and each != "0000":
            list(info.values())[len(info.values())-1].setdefault("hours",round(hr/60, 1))
            list(info.values())[len(info.values())-1].setdefault("toHr", pivot[0])
            hr = 0
            display = True
        hr = hr+1
        if display == True:
            if data[each] != None:
                info[each] = {"workType":data[each]["workType"], "note":data[each]["note"]}
            else:
                info[each] = {"workType":"Unallocated","note":""}
            display = False
        pivot = (each,data[each])
    list(info.values())[len(info.values())-1].setdefault("hours",round(hr/60, 1))
    list(info.values())[len(info.values())-1].setdefault("toHr", "2400")
    #
    print("-"*60)
    table = PrettyTable(["From", "To", "Work Type", "Hours Spend", "Note"])
    work_type = []
    hours_spend = []
    util = 0
    slack = 0
    unalloc = 0
    for each in info:
        if info[each]["workType"] in ["reading", "coding", "maths"]:
            util = util + info[each]["hours"]
        if info[each]["workType"] in ["surfing", "watching", "drawing"]:
            slack= slack + info[each]["hours"]
        if info[each]["workType"] == "Unallocated":
            unalloc = unalloc + info[each]["hours"]
        table.add_row([each, info[each]["toHr"], info[each]["workType"],info[each]["hours"],info[each]["note"]])
        work_type.append(info[each]["workType"])
        hours_spend.append(info[each]["hours"])
    print(table)
    hours_spend = [(x/24)*100 for x in hours_spend]
    fig1, ax1 = plt.subplots()
    ax1.pie(hours_spend, labels = work_type, autopct='%1.1f%%')
    ax1.title.set_text("Date: "+date)
    print("Productive Hours: "+str(util)+" ("+str(round(util/24, 3)*100)+" %)")
    print("Slacking Hours: "+str(slack)+" ("+str(round(slack/24, 3)*100)+" %)")
    print("Unallocated Hours: "+str(unalloc)+" ("+str(round(unalloc/24, 3)*100)+" %)")
    plt.show()

def analyze(worktype, days):
    start = datetime.today() - timedelta(days=days)
    if len(os.listdir("./files")) > 0:
        avail_start = datetime.strptime(os.listdir("./files").pop(0).split(".")[0],"%y-%m-%d")
        delta = start - avail_start
        if delta.days > 0 :
            avail_start = start
        print("Starting analysis from {}".format(avail_start.strftime("%y-%m-%d")))
        all = []
        while avail_start < datetime.today() - timedelta(days=1):
            data = {}
            try:
                with open("./files/"+avail_start.strftime("%y-%m-%d")+".json", "r+") as f:
                    data = json.load(f)
            except FileNotFoundError:
                print("{} file not found".format(avail_start.strftime("%y-%m-%d")+".json"))
                avail_start += timedelta(days=1)
                continue
            #
            mins = 0
            for i in data.keys():
                each = data[i]
                if each != None:
                    if each["workType"] in worktype:
                        mins += 1
            all.append(mins/60)
            avail_start += timedelta(days=1)
        print("Calculated {} data for {} days. Total hours: {:.3f} hours ({:.3f} %)".format(worktype, len(all), sum(all), (sum(all)/(len(all)*24))*100))
        print("min {:.3f} hrs max {:.3f} hrs avg {:.3f} hrs".format(min(all), max(all), sum(all)/len(all)))
    else:
        print("no log files")

if __name__ == '__main__':
    CHOICES = ["add", "remove", "view", "analyze"]
    WORKTYPE = ["sleeping", "office work", "reading book", "coding", "custom"]
    parser = argparse.ArgumentParser(description="Welcome to shuparb's timesheet!")
    parser.add_argument("-a", "--action", choices=CHOICES,help="Action to perform", required=True)
    parser.add_argument("-t", "--timestamp", nargs=2, help="Start & End timestamp of activity (24hrs format=HHMM)")
    parser.add_argument("-w", "--worktype", choices=WORKTYPE, help="Type of work you've done")
    parser.add_argument("-n", "--note", help="Any remark")
    parser.add_argument("-d", "--date", help="Specify date (format=YY-MM-DD)")
    parser.add_argument("--days", help="Number of days to analyze")
    args = parser.parse_args()
    datepat = re.compile(r'[\d]{2}-[\d]{2}-[\d]{2}')
    if args.date != None and re.fullmatch(datepat, args.date) == None:
        print("ERR: Wrong date pattern: {}".format(args.date))
        exit(1)
    date = datetime.today().strftime("%y-%m-%d") if args.date == None else args.date
    # creating required directories & files
    if "files" not in os.listdir():
        os.mkdir("files")
    if date+".json" not in os.listdir("./files") and args.action != "view":
        with open("./files/"+date+".json", "w") as f: 
            print("Creating date {}".format(date))
            json.dump(createDay(), f)
    elif date+".json" not in os.listdir("./files") and args.action == "view":
        print("Invalid date")
        exit(1)
    if args.action == "add":
        if args.worktype == None:
            print("ERR: Pls provide worktype to add")
            exit(1)
        if args.timestamp == None and len(args.timestamp) == 2:
            print("ERR: timestamp missing")
            exit(1)
        timepat = re.compile(r'[0-2][0-9][0-5][0-9] [0-2][0-9][0-5][0-9]')
        if re.fullmatch(timepat, args.timestamp[0]+" "+args.timestamp[1]) == None:
            print("ERR: timestamp invalid Pattern (format=HHMM HHMM)")
            exit(1)
        add(args.timestamp, workType=args.worktype, note=args.note)
    elif args.action == "remove":
        remove(args.timestamp)
    elif args.action == "view":
        view()
    elif args.action == "analyze":
        if args.days == None:
            args.days = "30"
        if args.worktype == None:
            choose = int(input("Choose work type: 1)Utilize 2)Slack 3)Office 4)Sleeping"))
            if choose == 1:
                analyze(["reading", "coding", "maths"], int(args.days))
                exit(0)
            if choose == 2:
                analyze(["surfing", "watching", "drawing"], int(args.days))
                exit(0)
            if choose == 3:
                analyze(["office"], int(args.days))
                exit(0)
            if choose == 4:
                analyze(["sleeping"], int(args.days))
                exit(0)
        analyze([args.worktype], int(args.days))
