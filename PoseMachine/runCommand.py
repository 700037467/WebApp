import os

def run(videoPath, videoName):
	path = os.getcwd()
	os.chdir("PoseMachine")
	os.chdir("VideoPose3D")
	os.chdir("inference")
	command = "python3 infer_video_d2.py --cfg COCO-Keypoints/keypoint_rcnn_R_101_FPN_3x.yaml --output-dir ../outputs --image-ext mp4 "+videoPath+videoName
	os.system(command)
	os.chdir("../")
	os.chdir("data")
	command = "python3 prepare_data_2d_custom.py -i ../outputs -o " + videoName
	os.system(command)
	os.chdir("../")
	command = "python3 run.py -d custom -k "+videoName+ " -arc 3,3,3,3,3 -c checkpoint --evaluate pretrained_h36m_detectron_coco.bin --render --viz-subject "+videoName+" --viz-action custom --viz-camera 0 --viz-video "+videoPath+videoName+ " --viz-output "+ videoName+" --viz-size 6"
	os.system(command)

	os.system("python3 openNpy.py")
	
	command = "python3 SetPelvisToOrigin.py -p "+videoPath + " -n " + videoName
	os.system(command)
	os.chdir(path)

if __name__ == '__main__':
	run("/Users/azaelfang/Desktop/Y3T1\ 2022/fyp/WebApp/PoseMachine/VideoPose3D/videos","w1.mp4")