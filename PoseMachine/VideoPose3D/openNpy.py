import pickle
import numpy as np
import pandas as pd
"""
input_keypoints = np.load('input_keypoints.npy', allow_pickle=True)
keypoints_metadata = np.load('keypoint_metadata.npy', allow_pickle=True)
print(input_keypoints)
print("---")
print(keypoints_metadata)
print("---")


anim_output = np.load('anim_output.npy',allow_pickle=True)
print(type(anim_output))
for a in anim_output.item():
    for b in anim_output.item()[a]:
        # print(len(b))
        print(b[0])
"""
A = np.load('anim_output.npy',allow_pickle=True)
count = 0
joints = ["Mid Hip","Right Hip", "Right Knee", "Right Ankle", "Left Hip", "Left Knee", "Left Ankle", "Waist", "Mid Shoulder", "Head",
            "Nose", "Left Shoulder", "Left Elbow", "Left Wrist", "Right Shoulder", "Right Elbow", "Right Wrist"]
label = ["14","8","10","12","7","9","11","-","13","-",
            "0","1","3","5","2","4","6"]
parts = ["Left Hand", "Right Hand", "Left Leg", "Right Leg", "Body"]

data = []
print(A.tolist()['Reconstruction'])

for time in A.tolist()['Reconstruction']:
    col = []
    for c, part in enumerate(parts):
        if (c==4):
            data.append([count, part, joints[0],label[0], time[0][0], time[0][1],time[0][2]])
            data.append([count, part, joints[7],label[7], time[7][0], time[7][1],time[7][2]])
            data.append([count, part, joints[8],label[8], time[8][0], time[8][1],time[8][2]])
            data.append([count, part, joints[9],label[9], time[9][0], time[9][1],time[9][2]])
            data.append([count, part, joints[10],label[10], time[10][0], time[10][1],time[10][2]])
        if (c==0):
            data.append([count, part, joints[8],"-", time[8][0], time[8][1],time[8][2]])
            data.append([count, part, joints[11],label[11], time[11][0], time[11][1],time[11][2]])
            data.append([count, part, joints[12],label[12], time[12][0], time[12][1],time[12][2]])
            data.append([count, part, joints[13],label[13], time[13][0], time[13][1],time[13][2]])
        if (c==1):
            data.append([count, part, joints[8],"-", time[8][0], time[8][1],time[8][2]])
            data.append([count, part, joints[14],label[14], time[14][0], time[14][1],time[14][2]])
            data.append([count, part, joints[15],label[15], time[15][0], time[15][1],time[15][2]])
            data.append([count, part, joints[16],label[16], time[16][0], time[16][1],time[16][2]])
        if (c==2):
            data.append([count, part, joints[0],"-", time[0][0], time[0][1],time[0][2]])
            data.append([count, part, joints[4],label[4], time[4][0], time[4][1],time[4][2]])
            data.append([count, part, joints[5],label[5], time[5][0], time[5][1],time[5][2]])
            data.append([count, part, joints[6],label[6], time[6][0], time[6][1],time[6][2]])
        if (c==3):
            data.append([count, part, joints[0],"-", time[0][0], time[0][1],time[0][2]])
            data.append([count, part, joints[1],label[1], time[1][0], time[1][1],time[1][2]])
            data.append([count, part, joints[2],label[2], time[2][0], time[2][1],time[2][2]])
            data.append([count, part, joints[3],label[3], time[3][0], time[3][1],time[3][2]])
    count+=1
""""
    for joint, plot in enumerate(time):
        data.append([count,joints[joint], plot[0],plot[1],plot[2]])
   
    count += 1
"""


column_names = ["Time", "Parts","Label", "Joint", "X", "Y", "Z"]
df = pd.DataFrame(data, columns=column_names)

df.to_csv("data.csv")

