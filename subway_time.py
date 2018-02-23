import csv
import string
from datetime import datetime,timedelta,date
import geocoder
"""
THINGS TO DO:
    -LOOK INTO KEEPING TRACK OF TIME
    -MAKE SURE CALCULATIONS ARE CORRECT
"""

def write_to_file(arr,fil):
    with open(fil,'w+') as csvOne:
        one = csv.writer(csvOne)
        for x in arr:
            one.writerows([x])

def sub_member(rowO,rowA,i):
    a = int(rowO[i]) - int(rowA[i])
    if a < 0:
        return 0
    return a

def add_member(rowO,rowA,i):
    """
    Adds up two members of a row by converting them to ints, adding them, and then returning the string version of the sum
    """
    a = int(rowO[i]) + int(rowA[i])
    return str(a)

def time_step_one(inp, outp):
    arr_one = []
    with open(inp,'r') as csvOne:
        one = csv.reader(csvOne)
        arr_one.append(one.next())
        previous = one.next()
        arr_one[0].pop(7)
        accum_entries = 0
        accum_exits = 0
        make_sure = 0
        turnstile = "Initialized"
        for x in one:
            if x[7][0] == "0" and  x[7][1] == "3" and make_sure > 0 and turnstile == x[2]:
                keep = previous
                accum_entries = sub_member(x,previous,9) + accum_entries
                accum_exits = sub_member(x,previous,10) + accum_exits
                keep[9] = str(accum_entries)
                keep[10] = str(accum_exits)
                keep.pop(7)
                arr_one.append(keep)
                accum_entries = 0
                accum_exits = 0
            elif turnstile != x[2] and make_sure > 0:
                keep = previous
                keep[9] = str(accum_entries)
                keep[10] = str(accum_exits)
                keep.pop(7)
                arr_one.append(keep)
                accum_entries = 0
                accum_exits = 0
            else:
                make_sure += 1
                accum_entries = sub_member(x,previous,9) + accum_entries
                accum_exits = sub_member(x,previous,10) + accum_exits
            previous = x
            turnstile = x[2]
    
    write_to_file(arr_one,outp)
    
def set_date(firstDay):
    """
    Creates string m d and y for first date so then datehelp can create
    6 more consecutive date strings
    """
    month = int(firstDay[0] + firstDay[1])
    day = int(firstDay[3] + firstDay[4])
    year = int(firstDay[6] + firstDay[7] + firstDay[8] + firstDay[9])
    days = date_help(month,day,year)
    return days
    
  
def pad_zeros(num):
    """
    Returns string of num with 0 in front if num is less than 10
    """
    if(num < 10):
        return "0" + str(num)
    else:
        return str(num)


def date_help(m,d,y):
    """
    Takes argument starting date separated into m d and y and creates array of strings of dates up to 6 days afterwards
    for a total of 7 uniformly formatted date strings
    """
    dates = []
    base = datetime(year = y,month = m, day = d)
    dates.append(pad_zeros(base.month) + "/" + pad_zeros(base.day) + "/" + pad_zeros(base.year))
    for i in range(0,6):
        base += timedelta(days=1)
        dates.append(pad_zeros(base.month) + "/" + pad_zeros(base.day) + "/" + pad_zeros(base.year))
    return dates

def return_date(date, dates):
    """
    returns place of date in array dates
    """
    for x in range(0,7):
        if dates[x] == date:
            return x
    return (-1)

def sort_date(inp,out_name):
    """
    Creates 7 
    """
    tot = []
    day_one = []
    day_two = []
    day_three = []
    day_four = []
    day_five = []
    day_six = []
    day_seven = []
    dates = []
    with open(inp,'r') as csvOne:
        one = csv.reader(csvOne)
        fieldNames = map(string.strip,one.next())
        day_one.append(fieldNames)
        day_two.append(fieldNames)
        day_three.append(fieldNames)
        day_four.append(fieldNames)
        day_five.append(fieldNames)
        day_six.append(fieldNames)
        day_seven.append(fieldNames)
        for x in one:
            tot.append(x)
        f_date = tot[0][6]
        dates = set_date(f_date)
        for x in tot:
            d = return_date(x[6],dates)
            if d >= 0:
                if d == 0:
                    day_one.append(x)
                elif d == 1:
                    day_two.append(x)
                elif d == 2:
                    day_three.append(x)
                elif d == 3:
                    day_four.append(x)
                elif d == 4:
                    day_five.append(x)
                elif d == 5:
                    day_six.append(x)
                elif d == 6:
                    day_seven.append(x)
                    
    for x in range(0,7):
        name = out_name +  dates[x][0] + dates[x][1] + dates[x][3] + dates[x][4] + ".txt"
        with open(name,'w+') as csvTwo:
            one = csv.writer(csvTwo)
            if x == 0:
                for y in day_one:
                    one.writerows([y])
            elif x == 1:
                for y in day_two:
                    one.writerows([y])
            elif x == 2:
                for y in day_three:
                    one.writerows([y])
            elif x == 3:
                for y in day_four:
                    one.writerows([y])
            elif x == 4:
                for y in day_five:
                    one.writerows([y])
            elif x == 5:
                for y in day_six:
                    one.writerows([y])
            elif x == 6:
                for y in day_seven:
                    one.writerows([y])

def turn_to_station(inp,outp):
    """Rolls up individual turnstiles into stations.
    Geocodes each station at the end
    """
    arr = []
    with open (inp,'r') as csvOne:
        one = csv.reader(csvOne)
        arr.append(one.next())
        arr[0].append("Latitude")
        arr[0].append("Longitude")
        arr[0].pop(2)
        while True:
            accum_entries = 0
            accum_exits = 0
            try:
                previous = one.next()
            except StopIteration:
                break
            rowRead = one.next()
            while rowRead[3] == previous[3]:
                accum_entries = accum_entries + int(rowRead[8])
                accum_exits = accum_exits + int(rowRead[9])
                previous = rowRead
                try:
                    rowRead = one.next()
                except StopIteration:
                    break

            previous.pop(2)
            previous.pop(7)
            previous.pop(7)
            lat = add_geo(previous[2] + ' ' + previous[3] + ", New York")
            previous.append(str(accum_entries))
            previous.append(str(accum_exits))
            if lat is not None:
                previous.append(str(lat[0]))
                previous.append(str(lat[1]))
            arr.append([previous])

    write_to_file(arr,outp) 


def add_geo(str1):
    """
        Geocodes input.
    """
    g = geocoder.google(str1)
    return g.latlng



def  main():
    file_one = "/Users/williamnewman/Desktop/Research/DataFiles/Subway December Data/turnstile_161203.txt"
    file_two = "/Users/williamnewman/Desktop/Research/DataFiles/Subway December Data/turnstile_161210.txt"
    time_one = "/Users/williamnewman/Desktop/time_one.txt"
    glo = "/Users/williamnewman/Desktop/dates/subway"
    a1 = "/Users/williamnewman/Desktop/dates/subway1126.txt"
    d1 = "/Users/williamnewman/Desktop/dates/1126update.txt"
    a2 = "/Users/williamnewman/Desktop/dates/subway1127.txt"
    d2 = "/Users/williamnewman/Desktop/dates/1127update.txt"
    a3 = "/Users/williamnewman/Desktop/dates/subway1128.txt"
    d3 = "/Users/williamnewman/Desktop/dates/1128update.txt"
    a4 = "/Users/williamnewman/Desktop/dates/subway1129.txt"
    d4 = "/Users/williamnewman/Desktop/dates/1129update.txt"
    a5 = "/Users/williamnewman/Desktop/dates/subway1130.txt"
    d5 = "/Users/williamnewman/Desktop/dates/1130update.txt"
    a6 = "/Users/williamnewman/Desktop/dates/subway1201.txt"
    d6 = "/Users/williamnewman/Desktop/dates/1201update.txt"
    a7 = "/Users/williamnewman/Desktop/dates/subway1202.txt"
    d7 = "/Users/williamnewman/Desktop/dates/1202update.txt"
    time_step_one(file_one,time_one)
    sort_date(time_one,glo)
    turn_to_station(a1,d1)
    """turn_to_station(a2,d2)
    turn_to_station(a3,d3)
    turn_to_station(a4,d4)
    turn_to_station(a5,d5)
    turn_to_station(a6,d6)
    turn_to_station(a7,d7)
"""

    
    
    


if __name__ == "__main__": main()
