import pygame, sys
import random
import numpy as np
from pygame.locals import *
from Camera import Camera
from FileOI import *

def displacementOfMouse(base,current):
    basex, basey=base
    currentx, currenty=current
    return (basey-currenty,basex-currentx)
def getCentralCoordinate(displayArea):
    topleft,bottomright=displayArea
    topleft_x,topleft_y=topleft
    bottomright_x,bottomright_y=bottomright
    center_x=(topleft_x + bottomright_x) / 2
    center_y=(topleft_y + bottomright_y) / 2
    return center_x,center_y


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

def rotation_zAxis(matrix,alpha):
    rotationMatrix=np.array([[np.cos(alpha), -np.sin(alpha), 0],
                    [np.sin(alpha), np.cos(alpha), 0],
                    [0, 0, 1]])
    ans=np.dot(rotationMatrix,matrix)

    return ans
def pixelToAngleConversion(pixels):
    return pixels*2*np.pi/pixelPerRound

def print_text(font, x, y, text, color=(0, 0, 0)):
    """打印字体函数"""
    img_text = font.render(text, True, color)
    screen.blit(img_text, (x, y))

def pointProjection(baseMatrix,point):
    point=tuple3ToArray(point)

    vectorT=point-np.dot(point, baseMatrix[:,1]) * baseMatrix[:,1]

    ans=np.dot(baseMatrix.T,vectorT)

    return ans[0],ans[2]
def tuple3ToArray(tuple):
    x,y,z=tuple

    return np.array([x,y,z])

def array3ToTuple(array):
    x = round(array[0][0], 5)
    y = round(array[1][0], 5)
    z = round(array[2][0], 5)
    return (x,y,z)


if __name__ == "__main__":
    pygame.init()
    # 字体
    font1 = pygame.font.SysFont("arial", 18)
    # 鼠标的移动位置
    """mouse_x = mouse_y = 0
    move_x = move_y = 0
    mouse_down = mouse_up = 0
    mouse_down_x = mouse_down_y = 0
    mouse_up_x = mouse_up_y = 0"""
    screen = pygame.display.set_mode((640, 500))
    pygame.display.set_caption("3DEngine_demo")
    img = pygame.image.load("E:\\3DEngine_demo\\logo.png")
    pygame.display.set_icon(img)

    filePath="data/test.csv"
    points,lines=readFile(filePath)

    directionSignFilePath="data/DirectionSign.csv"
    pointsDirectionSign, linesDirectionSign = readFile(directionSignFilePath)

    positionBase = (0, 0)
    currentMousePosition = (0, 0)

    displayArea = ((0, 0), (300, 300))
    centerCoordinate = getCentralCoordinate(displayArea)

    unitLength = 75

    pixelPerRound = 500

    cameraMatrix = np.array([[1, 0, 0],
                             [0, 1, 0],
                             [0, 0, 1]])

    baseCameraMatrix = np.array([[1, 0, 0],
                                 [0, 1, 0],
                                 [0, 0, 1]])
    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                currentMousePosition = event.pos
                # move_x,move_y = event.rel
            elif event.type == MOUSEBUTTONDOWN:
                positionBase = event.pos
                # mouse_down = event.button
            elif event.type == MOUSEBUTTONUP:
                baseCameraMatrix = cameraMatrix
                # mouse_up = event.button
                # mouse_up_x, mouse_up_y = event.pos

        left, middle, right = pygame.mouse.get_pressed()

        screen.fill((255, 255, 255))

        displacementVector_x, displacementVector_y = displacementOfMouse(positionBase, currentMousePosition)
        print_text(font1, 0, 280, u"relative dispalcement: " + str(displacementVector_x) + "," + str(
            displacementVector_y) + "  Based on Coordinate: " + str(positionBase))
        print_text(font1, 0, 300, u"current coordinate: " + str(currentMousePosition))
        rotationAngle_x = pixelToAngleConversion(displacementVector_x)
        rotationAngle_y = pixelToAngleConversion(displacementVector_y)

        print_text(font1, 0, 340, u"Rotation(in radian):" + str(rotationAngle_x) + "," + str(rotationAngle_y))

        if left == True:
            cameraMatrix = rotation_zAxis(rotation_yAxis(baseCameraMatrix, rotationAngle_x), rotationAngle_y)

        for line in lines:
            x0,y0,x1,y1=line.projectedTo(cameraMatrix)
            endpoint0 = [unitLength * x0 + centerCoordinate[0], -unitLength * y0 + centerCoordinate[1]]
            endpoint1 = [unitLength * x1 + centerCoordinate[0], -unitLength * y1 + centerCoordinate[1]]

            pygame.draw.line(screen, line.color, endpoint0, endpoint1, line.width)

        coordinateSystemCenter = (300, 200)
        for line in linesDirectionSign:
            x0,y0,x1,y1=line.projectedTo(cameraMatrix)
            endpoint0 = [unitLength * x0 + coordinateSystemCenter[0], -unitLength * y0 + coordinateSystemCenter[1]]
            endpoint1 = [unitLength * x1 + coordinateSystemCenter[0], -unitLength * y1 + coordinateSystemCenter[1]]
            pygame.draw.aaline(screen, line.color, endpoint0, endpoint1, True)

        """for point in testObject:
            x,y=pointProjection(baseMatrix=cameraMatrix,point=point)
            endpoint=[unitLength*x,unitLength*y]
            pygame.draw.aaline(screen, (0, 255, 0), [0, 0],endpoint, True)"""
        print_text(font1, 0, 380, u"[Camera Matrix] Projected onto xy-plane:  ")
        print_text(font1, 0, 400, u"Camera(x axis):" + str(cameraMatrix[:, 0]))
        print_text(font1, 0, 420, u"Camera(y axis):" + str(cameraMatrix[:, 1]))
        print_text(font1, 0, 440, u"Camera(z axis):" + str(cameraMatrix[:, 2]))

        """print_text(font1, 0, 0, u"鼠标事件")
        print_text(font1, 0, 20, u"鼠标的位置：" + str(mouse_x) + "," + str(mouse_y))
        print_text(font1, 0, 40, u"鼠标的偏移：" + str(move_x) + "," + str(move_y))
        print_text(font1, 0, 60, u"鼠标按下:" + str(mouse_down)
                   + "在" + str(mouse_down_x) + "," + str(mouse_down_y))
        print_text(font1, 0, 80, "鼠标松开:" + str(mouse_up)
                   + "在" + str(mouse_up_x) + "," + str(mouse_up_y))
        x, y = pygame.mouse.get_pos()
        print_text(font1, 0, 180, "鼠标位置:" + str(x) + "," + str(y))"""

        print_text(font1, 0, 460, "Mouse status(left,wheel,right):" + str(left) + "," + str(middle) + "," + str(right))
        pygame.display.update()