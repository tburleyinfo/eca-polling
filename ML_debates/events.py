import datetime
import json
import numpy as np
import pandas as pd


#Load Data
with open('debates.json') as debate:
    debates = json.loads(debate.read())

with open('performance.json') as perform: 
    performance = json.loads(perform.read())

with open('records.json') as records: 
    scores = json.loads(records.read()) #[negative, positive]

array = []
for date in performance.keys():
    array.append(date)

for date in scores.keys():
    if date not in array: 
       array.append(date)

pre = sorted(array, key=lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
#print("This is the schedule of dates. Use this to form series Y:", pre)


#Series X baseline: The occurance of a debate should shift the outcome in performance. 
#This means that any scores that happen outside of the debate positions are invalid. 
post = sorted(array, key=lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
for date in scores.keys(): 
    for element in range(len(post)):
        if post[element] == date: 
            entry = (date, post[element])
            post[element] = entry

series_X = []
for n in range(len(post)): 
    if isinstance(post[n], tuple): 
        series_X.append(1)
    else: 
        series_X.append(0)


#Series_Y: While series Y is always the same variable (performance change) there will be more iterations of this because of the number of debaters. 
#The threshold for a one is above 10%, an increase from the previous poll, or a significant descrease from the previous poll. 
seriesY = {}
bookPerformance = {}
save = ""
bookY = {}

#Load Polling Numbers for reference. They are already sorted by date(key).  
for num in range(len(pre)):
    key = pre[num]
    before = num - 1
    if key in performance.keys():
        for index in performance[key].keys():
            index = str(index)
            if index in seriesY.keys() and float(performance[key][index][1]) >= 10:
                seriesY[index][num] = 1
                bookPerformance[index][num] = performance[key][index][1]
            elif index not in seriesY.keys() and float(performance[key][index][1]) >= 10:
                seriesY[index] = [0]*len(pre)
                seriesY[index][num] = 1
                bookPerformance[index] = [0]*len(pre)
                bookPerformance[index][num] = performance[key][index][1]
            elif index in seriesY.keys() and float(performance[key][index][1]) < 10 or index not in performance[key].keys():
                seriesY[index][num] = 0
                bookPerformance[index][num] = bookPerformance[index][before]
            elif index not in seriesY.keys() and float(performance[key][index][1]) < 10 or index not in performance[key].keys():
                seriesY[index] = [0]*len(pre)
                seriesY[index][num] = 0
                bookPerformance[index] = [0]*len(pre)
                bookPerformance[index][num] = bookPerformance[index][before]
            else:
                seriesY[index] = [0]*len(pre)
                seriesY[index][num] = 0
            save = performance[key][index][1]

#Create Y series with conditions from polls. 
for num in range(len(pre)):
    key = pre[num]
    before = num - 1
    if key in performance.keys():
        for index in performance[key].keys():
            index = str(index)
            if index in bookY.keys() and float(performance[key][index][1]) >= 15:
                bookY[index][num] = 1
                bookPerformance[index][num] = performance[key][index][1]
            elif index not in bookY.keys() and float(performance[key][index][1]) >= 15:
                bookY[index] = [0]*len(pre)
                bookY[index][num] = 1
            elif index in bookY.keys() and (float(bookPerformance[index][num]) - float(bookPerformance[index][before])) >= 10:
                print(float(bookPerformance[index][num]) - float(bookPerformance[index][before]))
                bookY[index][num] = 1
                bookPerformance[index][num] = performance[key][index][1]
            elif index in bookY.keys() and (float(bookPerformance[index][before]) - float(bookPerformance[index][num])) >= 10:
                print(float(bookPerformance[index][before]) - float(bookPerformance[index][num]))
                bookY[index][num] = 1
                bookPerformance[index][num] = performance[key][index][1]
            elif index in bookY.keys() and float(performance[key][index][1]) < 10 or index not in performance[key].keys() or index not in bookPerformance.keys():
                bookY[index][num] = 0
            elif index not in bookY.keys() and float(performance[key][index][1]) < 10 or index not in performance[key].keys() or index not in bookPerformance.keys() or float(bookPerformance[index][num]) == float(bookPerformance[index][before]) :
                bookY[index] = [0]*len(pre)
                bookY[index][num] = 0
            elif index in bookY.keys() and float(bookPerformance[index][num]) == float(bookPerformance[index][before]):
                bookY[index][num] = 0
            else:
                bookY[index] = [0]*len(pre)
                bookY[index][num] = 0

#print(bookPerformance)
#print(bookY)

#Event Coincedence Analysis: Courtesy of pyunicorn
import ECA

print("[Precursor coincidence rate XY, Trigger coincidence rate XY, Precursor coincidence rate YX, Trigger coincidence rate YX]")
for key in bookY.keys(): 
    if key == 'Trump': continue
    x = np.asarray(series_X, dtype=np.float32)
    y = np.asarray(bookY[key], dtype=np.float32)
    v = ECA.ECA(x, y, 10, tau=1, ts1=None, ts2=None)
    if v[0] > 0: 
    	print("Trigger rates for", key, "is", v) 


print("The following candidates showed insignificant change in polling performance for analysis")
for key in bookY.keys():
    x = np.asarray(series_X, dtype=np.float32)
    y = np.asarray(bookY[key], dtype=np.float32)
    v = ECA.ECA(x, y, 10, tau=1, ts1=None, ts2=None)
    if v[0] == 0: print(key)








