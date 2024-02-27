import csv
import json
import time
from datetime import datetime

def getTime(str):
    if ( len(str) == 10 ):
         str = str + " 00:00"
    return int(datetime.strptime(str,'%d/%m/%Y %H:%M').timestamp())

def buildJSON(row):
    return {
        "startime": getTime(row[0]),
        "endtime": getTime(row[1]),
	"base": row[2],
        "userid": row[3]
    }


def main():
    count = 0
    with open('../data/call.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        header = next(reader)
        for row in reader:
            try:
                json = buildJSON(row)
                count = count + 1
            except Exception as err:
                print(row)
        
        print(count)

if __name__ == "__main__":
    main()
