# Timeshit
## Record minute-wise day's tasks
```
usage: timeshit.py [-h] -a {add,remove,view,analyze} [-t TIMESTAMP TIMESTAMP]
                   [-w {sleeping,office work,reading book,coding,custom}]
                   [-n NOTE] [-d DATE] [--days DAYS]

Welcome to shuparb's timesheet!

optional arguments:
  -h, --help            show this help message and exit
  -a {add,remove,view,analyze}, --action {add,remove,view,analyze}
                        Action to perform
  -t TIMESTAMP TIMESTAMP, --timestamp TIMESTAMP TIMESTAMP
                        Start & End timestamp of activity (24hrs format=HHMM)
  -w {sleeping,office work,reading book,coding,custom}, --worktype {sleeping,office work,reading book,coding,custom}
                        Type of work you've done
  -n NOTE, --note NOTE  Any remark
  -d DATE, --date DATE  Specify date (format=YY-MM-DD)
  --days DAYS           Number of days to analyze

```

## Adding new task/work 
```
python timeshit.py --action add --timestamp 0000 0500 --worktype sleeping --note "early today"
```

## Removing tasks
```
python timeshit.py --action remove --timestamp 0400 0500
````
## Display day's activity
![](https://github.com/ShubhamParab/Timeshit/blob/master/3.png)
