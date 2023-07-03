import csv
from Object import *

def toFloat(string):
    if string=="":
        return ""
    else:
        return float(string)
def toInt(string):
    if string=="":
        return ""
    else:
        return int(string)
def readFile(filePath):
    PointList = []
    LineList = []
    print("[info]: Reading",filePath, "=============================|")
    with open(filePath) as f:
        f_csv=csv.reader(f)

        readingPoints = False
        readingLines= False
        for item in f_csv:
            if item[0]=="Points":
                readingPoints=True
                readingLines=False
                continue
            elif item[0]=="Lines":
                readingPoints=False
                readingLines=True
                continue

            if readingPoints==True:
                color=toInt(item[4]),toInt(item[5]),toInt(item[6])
                try:
                    radius=toFloat(item[7])
                except:
                    radius=""
                point=Point(index=toInt(item[0]),
                            x=toFloat(item[1]), y=toFloat(item[2]), z=toFloat(item[3]),
                            color=color,
                            radius=radius)
                PointList.append(point)
                print(point.get_CoordinateInArray())
            elif readingLines==True:
                pointStartIndex=toInt(item[1])
                pointEndIndex=toInt(item[2])
                color = toInt(item[3]), toInt(item[4]), toInt(item[5])
                width = toFloat(item[6])
                line=Line(index=toInt(item[0]),
                          start=PointList[pointStartIndex],
                          end=PointList[pointEndIndex],
                          color=color,
                          width=width)
                LineList.append(line)
                print(line.get_VertexIndex())

    print("[info]: Finish Reading", filePath, "=============================|")
    return PointList,LineList
