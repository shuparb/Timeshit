import argparse
from datetime import datetime
import os
import json
from prettytable import PrettyTable
import matplotlib.pyplot as plt

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
    print("Viewing date's activity")
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
            list(info.values())[len(info.values())-1].setdefault("hours",round(hr/60, 2))
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
    list(info.values())[len(info.values())-1].setdefault("hours",round(hr/60, 2))
    list(info.values())[len(info.values())-1].setdefault("toHr", "2400")
    #
    print("-"*60)
    table = PrettyTable(["From", "To", "Work Type", "Hours Spend", "Note"])
    work_type = []
    hours_spend = []
    for each in info:
        table.add_row([each, info[each]["toHr"], info[each]["workType"],info[each]["hours"],info[each]["note"]])
        work_type.append(info[each]["workType"])
        hours_spend.append(info[each]["hours"])
    print(table)
    hours_spend = [(x/24)*100 for x in hours_spend]
    fig1, ax1 = plt.subplots()
    ax1.pie(hours_spend, labels = work_type, autopct='%1.1f%%')
    ax1.title.set_text("Date: "+date)
    plt.show()

if __name__ == '__main__':
    CHOICES = ["add", "remove", "view"]
    WORKTYPE = ["sleeping", "office work", "reading book", "coding", "custom"]
    parser = argparse.ArgumentParser(description="Welcome to shuparb's timesheet!")
    parser.add_argument("-A", "--action", choices=CHOICES,help="Action to perform", required=True)
    parser.add_argument("--timestamp", nargs=2, help="Start & End timestamp of activity (format=HHMM)")
    parser.add_argument("--worktype", choices=WORKTYPE, help="Type of work you've done")
    parser.add_argument("--note", help="Any remark")
    parser.add_argument("--date", help="Specify date (format=YY-MM-DD)")
    args = parser.parse_args()
    date = datetime.today().strftime("%y-%m-%d") if args.date == None else args.date
    # creating required directories & files
    if "files" not in os.listdir():
        os.mkdir("files")
    if date+".json" not in os.listdir("./files"):
        with open("./files/"+date+".json", "w") as f: 
            print("Creating date")
            json.dump(createDay(), f)
    #
    if args.action == "add":
        add(args.timestamp, workType=args.worktype, note=args.note)
    elif args.action == "remove":
        remove(args.timestamp)
    elif args.action == "view":
        view()
