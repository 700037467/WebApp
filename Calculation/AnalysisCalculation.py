
from turtle import width
from numpy import pad
import pandas
import numpy as np
from cmath import acos, atan, cos, pi



import math

import plotly.io as pio
import plotly.express as px

# generate 3D graph
def print3D(df, fileName):
    import matplotlib.pyplot as plt3D
    import matplotlib
    matplotlib.use('Agg')
    for az in range(-135, 180, 45):
        fig = plt3D.figure(figsize=(20,10))
       
        ax = fig.add_subplot(projection='3d')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        ax.tick_params(axis='both', which='minor', labelsize=3)
        for part in np.unique(df["Parts"].values):
            x = list(df[((df["Parts"] == part))]["X"])
            y = list(df[((df["Parts"] == part))]["Y"])
            z = list(df[((df["Parts"] == part))]["Z"])
            ax.plot3D(x,y,z,color='black', linewidth=0.5)
        ax.set_xlim(-1, 1)    
        ax.set_ylim(-1, 1)
        ax.set_zlim(-1, 1)
        ax.elev = 0

        ax.azim = az
        ax.grid(False)
        ax.set_yticks([])
        ax.set_xticks([])
        ax.set_zticks([])
        plt3D.tight_layout()
        fig.savefig(fileName+"3D"+str(az)+".png", dpi=300, bbox_inches='tight')  
        plt3D.close(fig)
        plt3D.figure().clear()
    
    
    
    

   
#coordinateN = [x,y,z]
# tanget rules
def twoPointsAngle(coordinateA:list, coordinateB:list):
    up = coordinateA[2] - coordinateB[2]
    down = pow(pow(coordinateA[0]- coordinateB[0],2)+pow(coordinateA[1]-coordinateB[1],2),0.5)
    delta = (180/pi)* math.atan(up/down)
    return round(delta, 2)

#obtain the vector from two coordinates
#line = [[x0, y0, z0], [x1,y1,z1]] or [[x0,y0],[x1,y1]]
def vector(line):
    if (len(line[0]) == 2):
        return [line[1][0]-line[0][0], line[1][1]-line[0][1]]
    return [line[1][0]-line[0][0], line[1][1]-line[0][1], line[1][2]-line[0][2]]


#coordinateN = [x,y,z]
#cosine rule
def twoLineAngleIn3Points(coordinateA:list, coordinateB:list, coordinateC:list):
    vectorA = vector([coordinateA, coordinateB])
    vectorB = vector([coordinateB, coordinateC])
    up = (vectorA[0]*vectorB[0]) + (vectorA[1]*vectorB[1]) + (vectorA[2]*vectorB[2])
    down = pow(pow(vectorA[0],2) + pow(vectorA[1],2) + pow(vectorA[2],2) ,0.5) * pow(pow(vectorB[0],2) + pow(vectorB[1],2) + pow(vectorB[2],2) ,0.5)
    delta = 180 - (180/pi) * math.acos(up/down)
    return round(delta,2)


def alignmentAngle(df, analysis):
    # 1 - back pack obliquity, 2 - shoulder obliquity, 3 - pelvis obqliquity
    bodyParts = {
        1: [13, 14],
        2: [1,2], 
        3: [7,8]
    }

    cor = getCoordinates(bodyParts.get(analysis), df)
    coordinateA = [cor[0][0], cor[0][1],cor[0][2]]
    coordinateB = [cor[1][0], cor[1][1],cor[1][2]]
    if (analysis == 1):
        return round((90 - twoPointsAngle(coordinateA,coordinateB)),2)
    else:
        return round(twoPointsAngle(coordinateA, coordinateB),2)


def limbsAngle (df, analysis):
    # 1 - left elbow angle, 2 - right elbow angle, 3 - left knee angle, 4 - right knee angle
    # 5 - left hip angle, 6 - right hip angle
    leftOrRight = {
        1: [1,3,5],
        2: [2,4,6],
        3: [7,9,11],
        4: [8,10,12],
        5: [1, 7 ,9],
        6: [2, 8, 10],
        
    }
    cor = getCoordinates(leftOrRight.get(analysis), df)
    return twoLineAngleIn3Points(cor[0], cor[1], cor[2])


def angleToDB(df):
    data = []
    data.append(limbsAngle(df,3))
    data.append(limbsAngle(df,4))
    data.append(limbsAngle(df,1))
    data.append(limbsAngle(df,2))
    data.append(alignmentAngle(df,3))
    data.append(alignmentAngle(df,2))
    data.append(alignmentAngle(df,1))
    return data
    


#coordinateN = [x, y, z]
def getLinePath(coordinateA, coordinateB):
    path = "M " + str(coordinateA[0]) + " " + str(coordinateA[2]) + " L " + str(coordinateB[0]) + " " + str(coordinateB[2])
    return path

def getCoordinates(bodyParts, df):
    cor = []
    for part in bodyParts:
        tmp = []
        tmp.append(df[(df["Label"] == str(part))]["X"].values[0])
        tmp.append(df[(df["Label"] == str(part))]["Y"].values[0])
        tmp.append(df[(df["Label"] == str(part))]["Z"].values[0])
        cor.append(tmp)

    return cor

#coordinateN = [x,y,z]
def plotAnglePath(coordinateA:list, coordinateB:list, coordinateC:list):

    centerPointAB = [(coordinateA[0] + coordinateB[0])/2, (coordinateA[2] + coordinateB[2])/2]
    centerPointBC = [(coordinateB[0] + coordinateC[0])/2, (coordinateB[2] + coordinateC[2])/2]
    centerPointABBC = [(centerPointAB[0]+centerPointBC[0])/2, (centerPointAB[1]+centerPointBC[1])/2]
    startPoint = [(centerPointAB[0]+coordinateB[0])/2, (centerPointAB[1]+coordinateB[2])/2]
    endPoint = [(centerPointBC[0]+coordinateB[0])/2, (centerPointBC[1]+coordinateB[2])/2]
    if ((coordinateB[0] < coordinateC[0])):
    #if pow(pow(coordinateB[0],2) + pow(coordinateB[1],2) + pow(coordinateB[2],2) ,0.5) <  pow(pow(coordinateC[0],2) + pow(coordinateC[1],2) + pow(coordinateC[2],2), 0.5):
        path = "M " + str(startPoint[0]) + " " + str(startPoint[1]) + " Q " + str(endPoint[0]) + " " + str(startPoint[1]) + " " + str(endPoint[0]) + " " + str(endPoint[1])
    else:
 
        path = "M " + str(startPoint[0]) + " " + str(startPoint[1]) + " Q " + str(startPoint[0]) + " " + str(endPoint[1]) + " " + str(endPoint[0]) + " " + str(endPoint[1])

    
    return path

def initFigure(df):
    fig = px.line(df, x=df["X"], y=df["Z"], color=df["Parts"])
    fig.update_layout(
        xaxis_range=[-1,1],
        yaxis_range=[-1,1],
        showlegend=False,
        
    plot_bgcolor='rgba(0,0,0,0)'
        )
    
    fig.update_traces(line=dict(
        color='black'),
        )
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black')
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black')
    return fig
    
   

def calculation(df, fileName):
    print3D(df, fileName)
    
    fig=initFigure(df)
    limbsAngle(df,fileName+"Analysis_leftElbow.jpg", fig, 1)
    limbsAngle(df,fileName+"Analysis_RightElbow.jpg", fig, 2)
    limbsAngle(df,fileName+"Analysis_LeftKneww.jpg", fig, 3)
    limbsAngle(df,fileName+"Analysis_RightKnee.jpg", fig, 4)
    alignmentAngle(df,fileName+"body.jpg", fig, 1)
    alignmentAngle(df,fileName+"shoulder.jpg", fig, 2)
    alignmentAngle(df,fileName+"pelvis.jpg", fig, 3)
    
