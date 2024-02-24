from datetime import datetime, timedelta

def datespan(startDate, endDate, delta=timedelta(days=1)):
    currentDate = startDate
    while currentDate < endDate:
        yield currentDate
        currentDate += delta

for timestamp in datespan(datetime(2007, 3, 30, 15, 30), 
                          datetime(2007, 3, 30, 18, 35), 
                           delta=timedelta(hours=1)):
    print(timestamp.year)