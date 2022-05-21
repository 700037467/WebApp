import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import plotly
import database as db
import plotly.express as px
import Calculation.AnalysisCalculation as ac
from plotly.subplots import make_subplots

def angleFlexionOrExtension(angle):
    if (angle < 90):
        return "Extension"
    return "Flexion"
    

def proceedAnalysis(filename):
    df = pd.read_csv(filename)
    maxFrame = int((df["Time"]).max())
    df["Angle"] = ""
    df["Analysis"] = ""
    df["Status"] = ""
    
    count = 1
    for time in range(maxFrame+1):
        dfTmp = df[df["Time"] == time]
        for i, row in dfTmp.iterrows():
            label = row["Label"]
            if (label == str(1)):
                df.at[i,'Analysis'] = float(ac.alignmentAngle(dfTmp, 2))
                df.at[i,'Angle'] = "Shoulder Alignment"
                
            elif (label == str(3)):
                angle = float(ac.limbsAngle(dfTmp, 1))
                df.at[i,'Analysis'] = angle
                df.at[i,'Angle'] = "Left Elbow Angle"
                df.at[i,'Status'] = angleFlexionOrExtension(angle)
            elif (label == str(4)):
                df.at[i,'Analysis'] = float(ac.limbsAngle(dfTmp, 2))
                df.at[i,'Angle'] = "Right Elbow Angle"
                df.at[i,'Status'] = angleFlexionOrExtension(angle)
            elif (label == str(7)):
                df.at[i,'Analysis'] = float(ac.limbsAngle(dfTmp, 5))
                df.at[i,'Angle'] = "Left Hip Angle"
                df.at[i,'Status'] = angleFlexionOrExtension(angle)
            elif (label == str(8)):
                df.at[i,'Analysis'] = float(ac.limbsAngle(dfTmp, 6))
                df.at[i,'Angle'] = "Right Hip Angle"
                df.at[i,'Status'] = angleFlexionOrExtension(angle)
            elif (label == str(9)):
                df.at[i,'Analysis'] = float(ac.limbsAngle(dfTmp, 3))
                df.at[i,'Angle'] = "Left Knee Angle"
                df.at[i,'Status'] = angleFlexionOrExtension(angle)
            elif (label == str(10)):
                df.at[i,'Analysis'] = float(ac.limbsAngle(dfTmp, 4))
                df.at[i,'Angle'] = "Right Knee Angle"
                df.at[i,'Status'] = angleFlexionOrExtension(angle)
            elif (label == str(13)):
                df.at[i,'Analysis'] = float(ac.alignmentAngle(dfTmp, 1))
                df.at[i,'Angle'] = "Body Alignment"
            elif (label == str(14)):
                df.at[i,'Analysis'] = float(ac.alignmentAngle(dfTmp, 3))
                df.at[i,'Angle'] = "Pelvis Obliquity"
            else:
               df.at[i,'Analysis'] = ("")
               df.at[i,'Angle'] = "No angle provided"
            count += 1  

    return df
            
def humanModel(df):
    parts = df["Parts"].unique()

    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{'type': 'scatter'}, {'type': 'scatter3D'}]]
           
        )
    timeRange = 500
    maxFrame = int((df["Time"]).max())+1
    time = int(maxFrame/timeRange)
    count = 0
    graphJson = {}

    while (count <= time):
        startFrame = count*timeRange
        endFrame = (count+1) * timeRange
        if ((endFrame > maxFrame) or (maxFrame <= endFrame + 10)):
            count += 1
            endFrame = maxFrame

        dftmp = df[(df["Time"] >= startFrame) & (df["Time"] < endFrame)]
        dfFirstFrame = dftmp[dftmp["Time"] == (dftmp["Time"]).min()]
        dfFirstFrame = dftmp[dftmp["Time"] == 0]

        for index, part in enumerate(parts):
            fig.add_trace(
                
                go.Scatter(x=dfFirstFrame[(dfFirstFrame["Parts"] == part)]["X"], 
                            y=dfFirstFrame[(dfFirstFrame["Parts"] == part)]["Z"], 
                            mode='lines+markers',
                            text = dfFirstFrame[dfFirstFrame["Parts"]==part]["Angle"] +"\n"+ dfFirstFrame[dfFirstFrame["Parts"]==part]["Status"],
                            customdata = dfFirstFrame[dfFirstFrame["Parts"]==part]["Analysis"],
                            hovertemplate = "%{text} <br>Degree: %{customdata}",
                            name=part,legendgroup=part,
                            marker=dict(color=px.colors.qualitative.Plotly[index])),
                row=1,col=1,
                
            )
            fig.add_trace(
                go.Scatter3d(x=dfFirstFrame[(dfFirstFrame["Parts"] == part)]["X"], 
                            y=dfFirstFrame[(dfFirstFrame["Parts"] == part)]["Y"], 
                            z=dfFirstFrame[(dfFirstFrame["Parts"] == part)]["Z"], 
                            mode='lines',
                            name=part,
                            legendgroup=part,showlegend=False,
                            marker=dict(color=px.colors.qualitative.Plotly[index])),
                row=1, col=2
            )
            
        sliders = [dict(steps= [dict(method= 'animate',
                            args= [[k],
                                    dict(mode= 'immediate',
                                    frame= dict( duration=0, redraw= True ),
                                            transition=dict( duration= 0)
                                            )
                                        ],
                                label=k
                                ) for k in range(int(startFrame),int(endFrame))], 
                    transition= dict(duration= 0),
                    x=0,
                    y=0,
                    currentvalue=dict(font=dict(size=12), visible=True, xanchor= 'center'),
                    len=1.0)
            ]
        updatemenus=[
                dict(
                    type = "buttons",
                    direction = "left",
                    x=0.11,
                    xanchor="left",
                    y=1.1,
                    yanchor="bottom",
                    buttons=list([
                        dict(label="Play",
                            method="animate",
                            args = [None, {
                                        "frame": {"duration": 100, "redraw": True},
                                        "fromcurrent": True, 
                                        "mode":"immediate",
                                        
                                        "transition": {"duration":100 ,"easing":"linear",}}]),
                        dict(label="Pause",
                            method="animate",
                            args = [[None], {
                                        "frame": {"duration": 0, "redraw": True},
                                        "fromcurrent": True, 
                                        "mode": "immediate", 
                                    
                                        "transition": {"duration": 0,"easing":"linear",}}]),
                                        ]))]
       
        frames = []
        for k in range(int(startFrame),int(endFrame)):
            frame = {}
            data = []
            for index, part in enumerate(parts):
                data.append(go.Scatter(
                            x=df[(df["Time"]==k) & (df["Parts"]==part)]["X"], 
                            y=df[(df["Time"]==k) & (df["Parts"]==part)]["Z"], 
                            text = df[(df["Time"]==k) & (df["Parts"]==part)]["Angle"] +"\n"+ df[(df["Time"]==k) & (df["Parts"]==part)]["Status"],
                            customdata = df[(df["Time"]==k) & (df["Parts"]==part)]["Analysis"],
                            hovertemplate = "%{text} <br>Degree: %{customdata}",
                            legendgroup=part,
                            marker=dict(color=px.colors.qualitative.Plotly[index])
                        ))
                data.append(go.Scatter3d(
                            x=df[(df["Time"]==k) & (df["Parts"]==part)]["X"], 
                            y=df[(df["Time"]==k) & (df["Parts"]==part)]["Y"], 
                            z=df[(df["Time"]==k) & (df["Parts"]==part)]["Z"], 
                            legendgroup=part,
                            marker=dict(color=px.colors.qualitative.Plotly[index])
        
                        ))
            frame["name"] = int(k)
            frame["traces"] = [0,1,2,3,4,5,6,7,8,9]
            frame["data"] = data
            frames.append(frame)
        
        fig.update_xaxes(range=[-1,1], row=1, col=1)
        fig.update_yaxes(range=[-1,1], row=1, col=1)
        fig.update_layout(scene = dict(
                    xaxis = dict(nticks=4, range=[-1,1],),
                     yaxis = dict(nticks=4, range=[-1,1],),
                     zaxis = dict(nticks=4, range=[-1,1],),)
                    
        )
        fig.update_layout(scene_aspectmode='cube', height=600)
        fig.update(frames=frames)
        fig['layout'].update(updatemenus=updatemenus,
        sliders=sliders)
        
        frameName = str(startFrame)+"-"+str(endFrame-1)            
        graphJson[frameName] = fig.to_json()
        count += 1

    return graphJson




def proceedGraphData(df):
   
    df['E'] = df.apply(lambda row: (pow(pow(row.X, 2)+pow(row.Y, 2)+pow(row.Z+1, 2),0.5)), axis=1)
    
 
    timeRange = 500
    maxFrame = (df["Time"]).max()+1
    time = int(maxFrame/timeRange)
    count = 0
    graphJson = {}
    while (count <= time):
        startFrame = count*timeRange
        endFrame = (count+1) * timeRange
        if ((endFrame > maxFrame) or (maxFrame <= endFrame + 10)):
            count += 1
            endFrame = maxFrame
        dftmp = df[(df["Time"] >= startFrame) & (df["Time"] < endFrame)]
        
        """
        figX = px.line(x=dftmp["Time"], y=dftmp["X"],color=dftmp["Joint"])
        figY = px.line(x=dftmp["Time"], y=dftmp["Y"],color=dftmp["Joint"])
        figZ = px.line(x=dftmp["Time"], y=dftmp["Z"],color=dftmp["Joint"])
        """
        figE = px.line(x=dftmp["Time"], y=dftmp["E"],color=dftmp["Joint"])
   
        frameName = str(startFrame)+"-"+str(endFrame-1) 
        graphJson[frameName]  = {}     
        """   
        graphJson[frameName]['X'] = figX.to_json()
        graphJson[frameName]['Y'] = figY.to_json()
        graphJson[frameName]['Z'] = figZ.to_json()
        """
        graphJson[frameName]['E'] = figE.to_json()

        count += 1
    return graphJson


def processAnalysis(conn, fileName):
    
    df = pd.read_csv(fileName)
    maxFrame = int((df["Time"]).max())

    
    for frame in range(maxFrame+1):
        data = []
        """
        frame INTEGER,
        leftkneeangle REAL,
        rightkneeangle REAL,
        leftelbowangle REAL,
        rightelbowangle REAL,
        pelvisalign REAL,
        shoulderalign REAL,
        bodyalign REAL
       """
        data.append(frame)
        dfTmp = df[df["Time"] == frame]
        data.extend(ac.angleToDB(dfTmp))
        db.insert_analysis_data(conn, data)
    
def generateComment(angle):
    if (angle >= -5 and angle <= 5):
        return "Correct Posture"
    else:
        return "Incorrect Posture"
        









