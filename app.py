

from datetime import datetime
import imp

import json
from flask import Flask, redirect, render_template, request, flash

from Calculation import AnalysisCalculation
import plotly.express as px
import pandas as pd
import os

import plotly
from flask import session
from werkzeug.utils import secure_filename
import database as db
import proceedHumanModel as hm
from PoseMachine import runCommand as pose






server = Flask(__name__)
server.secret_key = "super secret key"

path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'static/uploads')
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

server.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@server.route('/')
def index():
    return render_template('upload.html')

@server.route('/PoseMachine', methods=['GET', 'POST'])
def poseMachine():
    if request.method == 'POST':
        if 'videoFile' not in request.files:
            
            flash('No file part')
            return redirect(request.url)
        video = request.files['videoFile']
        if (video.filename == ''):
          
            flash('No file selected for uploading')
            return redirect(request.url)
        elif (video.filename.endswith('.mp4')):
           
            videoFileName = secure_filename(video.filename)
            video.save(os.path.join(server.config['UPLOAD_FOLDER'], videoFileName))
            session['videoName'] = videoFileName
            
            pose.run(server.config['UPLOAD_FOLDER']+"/", videoFileName)
            handleData(videoFileName+".csv")
            session['videoName'] = videoFileName
            session['fps'] = 50
            flash('File successfully uploaded')
            return redirect('/Analysis')

        else:
            flash('Only MP4 file is allowed.')
            return redirect(request.url)
        
    
    
def handleData(filename):
    filename = os.path.join(server.config['UPLOAD_FOLDER'], filename)
    df = hm.proceedAnalysis(filename)

    conn = db.connect_to_db()
    db.inithumanModelData(conn, df)
    db.initAnimationData(conn,hm.humanModel(df))  
    db.initGraph(conn, hm.proceedGraphData(df))
    db.close(conn)
    


@server.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        video = request.files['videoFile']
        fps = request.form.get('fps')
        if (file.filename == ''):
            flash('No file selected for uploading')
            return redirect(request.url)
        elif (file.filename.endswith('.csv')):
            filename = secure_filename(file.filename)
           
            start=datetime.now()
            file.save(os.path.join(server.config['UPLOAD_FOLDER'], filename))
            
            handleData(filename)
            print("Time: ",datetime.now() - start)
            flash('File successfully uploaded')
            
            if (video.filename != '' and video.filename.endswith('mp4')):
                videoFileName = secure_filename(video.filename)
                video.save(os.path.join(server.config['UPLOAD_FOLDER'], videoFileName))
                session['videoName'] = videoFileName
                session['fps'] = fps
            elif (video.filename != '' and not video.filename.endswith('mp4')):
                flash('Only MP4 file is allowed.')
                return redirect(request.url)
            return redirect('/Analysis')
        else:
            flash('Only CSV and MP4 file is allowed.')
            return redirect(request.url)

@server.route('/Analysis', methods=['GET', 'POST'])
def showModel():
    try:
        fps = 30
        video = session.get("videoName")
        if (not session.get("videoName")):
            video = ""
 
        if (session.get("fps")):
            fps = session.get("fps")
        
       
        conn = db.connect_to_db()

        humanModelJson = {}
        humanModelData = db.retrieveAnimationData(conn)
        for gData in humanModelData:
            humanModelJson[gData[0]] = {
                "data":json.loads(gData[1]),
                "layout" : json.loads(gData[2]),
                "frames":json.loads(gData[3])
            }

        graphData = db.retrieveGraph(conn)
        graphDataJson = {}
        for gData in graphData:
            graphDataJson[gData[0]] = {

                "e":json.loads(gData[1])
            }

        label = [1, 3, 4, 7, 8, 9, 10, 13,14]
        analysisData = db.retrieveAllAnalysis(conn)
        
        analysisData["Analysis"] = analysisData["Analysis"].astype(float)

        fig = px.line(analysisData,x='Time', y='Analysis',color='Angle')
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
        

            
        
        return render_template('AnalysisAndModel.html', 
                                graphsData=json.dumps(graphDataJson), 
                                videoName=video,fps=fps,
                                animData=json.dumps(humanModelJson),
                                shoulderAlign=round(db.retrieveAnalysisAverageFromLabel(conn, label[0]),2),
                            shoulderAlignComment = hm.generateComment(db.retrieveAnalysisAverageFromLabel(conn, label[0])),
                            leftElbowAngle=round(db.retrieveAnalysisAverageFromLabel(conn, label[1]),2),
                            rightElbowAngle=round(db.retrieveAnalysisAverageFromLabel(conn, label[2]),2),
                            leftHipAngle=round(db.retrieveAnalysisAverageFromLabel(conn, label[3]),2),
                            rightHipAngle=round(db.retrieveAnalysisAverageFromLabel(conn, label[4]),2),
                            leftKneeAngle = round(db.retrieveAnalysisAverageFromLabel(conn, label[5]),2),
                            rightKneeAngle=round(db.retrieveAnalysisAverageFromLabel(conn, label[6]),2),
                            bodyAlign=round(db.retrieveAnalysisAverageFromLabel(conn, label[7]),2),
                            bodyAlignComment = hm.generateComment(db.retrieveAnalysisAverageFromLabel(conn, label[7])),
                            pelvisAlign=round(db.retrieveAnalysisAverageFromLabel(conn, label[8]),2),
                            pelvisAlignComment = hm.generateComment(db.retrieveAnalysisAverageFromLabel(conn, label[8])),
                            analysisGraph = graphJSON)
    except Exception as e:
        return render_template('NoData.html', error=str(e))

@server.route('/Profile')
def showProfile():
    conn = db.connect_to_db()
    label = [1, 3, 4, 7, 8, 9, 10, 13,14]
    analysisData = db.retrieveAllAnalysis(conn)
    
    analysisData["Analysis"] = analysisData["Analysis"].astype(float)

    fig = px.line(analysisData,x='Time', y='Analysis',color='Angle')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    


    return render_template('Profile.html', 
                            shoulderAlign=round(db.retrieveAnalysisAverageFromLabel(conn, label[0]),2),
                            shoulderAlignComment = hm.generateComment(db.retrieveAnalysisAverageFromLabel(conn, label[0])),
                            leftElbowAngle=round(db.retrieveAnalysisAverageFromLabel(conn, label[1]),2),
                            rightElbowAngle=round(db.retrieveAnalysisAverageFromLabel(conn, label[2]),2),
                            leftHipAngle=round(db.retrieveAnalysisAverageFromLabel(conn, label[3]),2),
                            rightHipAngle=round(db.retrieveAnalysisAverageFromLabel(conn, label[4]),2),
                            leftKneeAngle = round(db.retrieveAnalysisAverageFromLabel(conn, label[5]),2),
                            rightKneeAngle=round(db.retrieveAnalysisAverageFromLabel(conn, label[6]),2),
                            bodyAlign=round(db.retrieveAnalysisAverageFromLabel(conn, label[7]),2),
                            bodyAlignComment = hm.generateComment(db.retrieveAnalysisAverageFromLabel(conn, label[7])),
                            pelvisAlign=round(db.retrieveAnalysisAverageFromLabel(conn, label[8]),2),
                            pelvisAlignComment = hm.generateComment(db.retrieveAnalysisAverageFromLabel(conn, label[8])),
                            analysisGraph = graphJSON
    )


@server.route('/Person')
def person():
    script_dir = os.path.dirname(__file__)
    filePath = 'static/Profile/'
    results_dir = os.path.join(script_dir, filePath)
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)
    personList = []
    for i in os.listdir(results_dir):
        if (i.endswith(".db")):
            personList.append(i[:-3])
    print(personList)
    return render_template("Person.html",
                        personList = json.dumps(personList)
                        )
          

"""
@server.route('/DoAnalysis/<f>')
def DoAnalysis(f):

    script_dir = os.path.dirname(__file__)
    filePath = 'static/Image/' + f + '/'
    results_dir = os.path.join(script_dir, filePath)
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)
    df = db.retrieveDataFrameFromFrame(f)
 
    imgList = {"threeD":[], "Analysis":[]}
    
    AnalysisCalculation.calculation(df, results_dir)
   
    for i in os.listdir(results_dir):
        if (i.startswith("3D")):
            imgList["threeD"].append(i)
        else:
            imgList["Analysis"].append(i)
    
    return json.dumps(imgList)




@server.route('/exportGraph/<startFrame>/<endFrame>/<joints>')
def exportGraph(startFrame, endFrame,joints):
    print("Joints", joints)
    print(type(joints))
    script_dir = os.path.dirname(__file__)
    filePath = 'static/Graph/'
    results_dir = os.path.join(script_dir, filePath)
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)
    df = pd.read_csv('data.csv')

    df = df[df['Time'].between(int(startFrame), int(endFrame))]
    tmp = []
    for joint in joints.split(','):
        tmp.append(df[df["Joint"] == joint])

    graphExport.generateThreeGraph(pd.concat(tmp), results_dir, joints.split(','))
    return ""

"""
    

if __name__ == '__main__':
  server.run_server(debug=True, port=8056)
