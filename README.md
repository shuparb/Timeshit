# Timeshit
## Record minute-wise day's tasks
```
usage: timeshit.py [-h] -A {add,remove,view} [--timestamp TIMESTAMP TIMESTAMP]
                   [--worktype {sleeping,office work,reading book,coding,custom}] [--note NOTE] [--date DATE]

Welcome to shuparb's timesheet!

optional arguments:
  -h, --help            show this help message and exit
  -A {add,remove,view}, --action {add,remove,view}
                        Action to perform
  --timestamp TIMESTAMP TIMESTAMP
                        Start & End timestamp of activity (format=HHMM)
  --worktype {sleeping,office work,reading book,coding,custom}
                        Type of work you've done
  --note NOTE           Any remark
  --date DATE           Specify date (format=YY-MM-DD)
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
