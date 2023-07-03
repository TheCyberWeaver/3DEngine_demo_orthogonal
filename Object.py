import numpy as np
class Point:
    def __init__(self,index,x,y,z,color=(0,0,0),radius=5):
        if color==("","",""):
            color=(0,0,0)
        if radius=="":
            radius=5
        self.Index=index
        self.XCoordinateOriginal=x
        self.YCoordinateOriginal=y
        self.ZCoordinateOriginal=z

        self.color=color
        self.radius=radius

        self.XCoordinateCameraMatrix = x
        self.YCoordinateCameraMatrix = y
        self.ZCoordinateCameraMatrix = z

        self.XCoordinateDisplay=0
        self.YCoordinateDisplay=1

    def get_CoordinateInArray(self):
        return np.array([self.XCoordinateOriginal,self.YCoordinateOriginal,self.ZCoordinateOriginal])

    def get_CoordinateInTuple(self):
        return self.XCoordinateOriginal,self.YCoordinateOriginal,self.ZCoordinateOriginal

    def projectedTo(self,baseMatrix):
        point = self.get_CoordinateInArray()

        vectorT = point - np.dot(point, baseMatrix[:, 1]) * baseMatrix[:, 1]

        ans = np.dot(baseMatrix.T, vectorT)

        self.XCoordinateDisplay=ans[0]
        self.YCoordinateDisplay = ans[2]

        return ans[0], ans[2]

class Line:
    def __init__(self,index,start,end,color=(0,0,0),width=5):

        if color==("","",""):
            color=(0,0,0)
        if width=="":
            width=5

        self.Index=index
        self.startPoint=start
        self.endPoint=end

        self.color=color

        self.width=width
    def set_color(self,RGB):
        self.color=RGB

    def get_VertexIndex(self):
        return self.startPoint.Index,self.endPoint.Index
    def projectedTo(self,matrix):
        x0,y0=self.startPoint.projectedTo(matrix)
        x1,y1=self.endPoint.projectedTo(matrix)
        return x0,y0,x1,y1
class Square:
    def __init__(self):
        pass
