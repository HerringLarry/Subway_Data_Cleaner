import csv
import numpy as np
import string
from difflib import SequenceMatcher
import fiona
from datetime import datetime,timedelta,date
import geocoder
"""
THINGS TO DO:
    -LOOK INTO KEEPING TRACK OF TIME
    -MAKE SURE CALCULATIONS ARE CORRECT
"""

def writeToFile(arr,fil):
    with open(fil,'w+') as csvOne:
        one = csv.writer(csvOne)
        for x in arr:
            one.writerows([x])

def subMember(rowO,rowA,i):
    a = int(rowO[i]) - int(rowA[i])
    if a < 0:
        return 0
    return a

def addMember(rowO,rowA,i):
    """
    Adds up two members of a row by converting them to ints, adding them, and then returning the string version of the sum
    """
    a = int(rowO[i]) + int(rowA[i])
    return str(a)

def timeStepOne(inp, outp):
    arrOne = []
    with open(inp,'r') as csvOne:
        one = csv.reader(csvOne)
        arrOne.append(one.next())
        previous = one.next()
        arrOne[0].pop(7)
        accumEntries = 0
        accumExits = 0
        makeSure = 0
        turnstile = "Initialized"
        for x in one:
            if x[7][0] == "0" and  x[7][1] == "3" and makeSure > 0 and turnstile == x[2]:
                keep = previous
                accumEntries = subMember(x,previous,9) + accumEntries
                accumExits = subMember(x,previous,10) + accumExits
                keep[9] = str(accumEntries)
                keep[10] = str(accumExits)
                keep.pop(7)
                arrOne.append(keep)
                accumEntries = 0
                accumExits = 0
            elif turnstile != x[2] and makeSure > 0:
                keep = previous
                keep[9] = str(accumEntries)
                keep[10] = str(accumExits)
                keep.pop(7)
                arrOne.append(keep)
                accumEntries = 0
                accumExits = 0
            else:
                makeSure += 1
                accumEntries = subMember(x,previous,9) + accumEntries
                accumExits = subMember(x,previous,10) + accumExits
            previous = x
            turnstile = x[2]
    
    writeToFile(arrOne,outp)
    
def setDate(firstDay):
    """
    Creates string m d and y for first date so then datehelp can create
    6 more consecutive date strings
    """
    month = int(firstDay[0] + firstDay[1])
    day = int(firstDay[3] + firstDay[4])
    year = int(firstDay[6] + firstDay[7] + firstDay[8] + firstDay[9])
    days = dateHelp(month,day,year)
    return days
    
  
def padZeros(num):
    """
    Returns string of num with 0 in front if num is less than 10
    """
    if(num < 10):
        return "0" + str(num)
    else:
        return str(num)


def dateHelp(m,d,y):
    """
    Takes argument starting date separated into m d and y and creates array of strings of dates up to 6 days afterwards
    for a total of 7 uniformly formatted date strings
    """
    dates = []
    base = datetime(year = y,month = m, day = d)
    dates.append(padZeros(base.month) + "/" + padZeros(base.day) + "/" + padZeros(base.year))
    for i in range(0,6):
        base += timedelta(days=1)
        dates.append(padZeros(base.month) + "/" + padZeros(base.day) + "/" + padZeros(base.year))
    return dates

def returnDate(date, dates):
    """
    returns place of date in array dates
    """
    for x in range(0,7):
        if dates[x] == date:
            return x
    return (-1)

def sortDate(inp,outName):
    """
    Creates 7 
    """
    tot = []
    dayOne = []
    dayTwo = []
    dayThree = []
    dayFour = []
    dayFive = []
    daySix = []
    daySeven = []
    dates = []
    with open(inp,'r') as csvOne:
        one = csv.reader(csvOne)
        fieldNames = map(string.strip,one.next())
        dayOne.append(fieldNames)
        dayTwo.append(fieldNames)
        dayThree.append(fieldNames)
        dayFour.append(fieldNames)
        dayFive.append(fieldNames)
        daySix.append(fieldNames)
        daySeven.append(fieldNames)
        for x in one:
            tot.append(x)
        print tot[0] 
        fDate = tot[0][6]
        dates = setDate(fDate)
        for x in tot:
            d = returnDate(x[6],dates)
            if d >= 0:
                if d == 0:
                    dayOne.append(x)
                elif d == 1:
                    dayTwo.append(x)
                elif d == 2:
                    dayThree.append(x)
                elif d == 3:
                    dayFour.append(x)
                elif d == 4:
                    dayFive.append(x)
                elif d == 5:
                    daySix.append(x)
                elif d == 6:
                    daySeven.append(x)
                    
    for x in range(0,7):
        name = outName +  dates[x][0] + dates[x][1] + dates[x][3] + dates[x][4] + ".txt"
        with open(name,'w+') as csvTwo:
            one = csv.writer(csvTwo)
            if x == 0:
                for y in dayOne:
                    one.writerows([y])
            elif x == 1:
                for y in dayTwo:
                    one.writerows([y])
            elif x == 2:
                for y in dayThree:
                    one.writerows([y])
            elif x == 3:
                for y in dayFour:
                    one.writerows([y])
            elif x == 4:
                for y in dayFive:
                    one.writerows([y])
            elif x == 5:
                for y in daySix:
                    one.writerows([y])
            elif x == 6:
                for y in daySeven:
                    one.writerows([y])

def turnToStation(inp,outp):
    arr = []
    with open (inp,'r') as csvOne:
        one = csv.reader(csvOne)
        arr.append(one.next())
        arr[0].append("Latitude")
        arr[0].append("Longitude")
        arr[0].pop(2)
        while True:
            accumEntries = 0
            accumExits = 0
            try:
                previous = one.next()
            except StopIteration:
                break
            rowRead = one.next()
            while rowRead[3] == previous[3]:
                accumEntries = accumEntries + int(rowRead[8])
                accumExits = accumExits + int(rowRead[9])
                previous = rowRead
                try:
                    rowRead = one.next()
                except StopIteration:
                    break

            previous.pop(2)
            previous.pop(7)
            previous.pop(7)
            lat = addGeo(previous[2] + ' ' + previous[3] + ", New York")
            previous.append(str(accumEntries))
            previous.append(str(accumExits))
            if lat is not None:
                previous.append(str(lat[0]))
                previous.append(str(lat[1]))
            arr.append([previous])

    writeToFile(arr,outp) 


def addGeo(str1):
    g = geocoder.google(str1)
    return g.latlng

def  main():
    fileOne = "/Users/williamnewman/Desktop/Research/DataFiles/Subway December Data/turnstile_161203.txt"
    fileTwo = "/Users/williamnewman/Desktop/Research/DataFiles/Subway December Data/turnstile_161210.txt"
    timeOne = "/Users/williamnewman/Desktop/timeOne.txt"
    glo = "/Users/williamnewman/Desktop/dates/subway"
    d1 = "/Users/williamnewman/Desktop/dates/subway1126.txt"
    d2 = "/Users/williamnewman/Desktop/dates/1126update.txt"
    timeStepOne(fileOne,timeOne)
    sortDate(timeOne,glo)
    turnToStation(d1,d2)


    
    
    


if __name__ == "__main__": main()
