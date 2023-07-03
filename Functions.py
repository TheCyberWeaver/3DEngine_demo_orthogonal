import numpy as np

def rotation_xAxis(matrix,alpha):
    rotationMatrix = np.array([[1, 0, 0],
                      [0, np.cos(alpha), -np.sin(alpha)],
                      [0, np.sin(alpha), np.cos(alpha)]])
    ans = np.dot(rotationMatrix, matrix)

    return ans


def rotation_yAxis(matrix,alpha):
    rotationMatrix = np.array([[np.cos(alpha), 0, np.sin(alpha)],
                      [0, 1, 0],
                      [-np.sin(alpha), 0, np.cos(alpha)]])
    ans = np.dot(rotationMatrix, matrix)
    return ans
baseCameraMatrix=np.array([[1,0,0],
                           [0,1,0],
                           [0,0,1]])

rotationAngle_x=0
rotationAngle_y=0
cameraMatrix = rotation_yAxis(rotation_xAxis(baseCameraMatrix,rotationAngle_x),rotationAngle_y)


print(cameraMatrix)