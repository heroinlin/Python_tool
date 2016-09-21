# -*- coding: utf-8 -*-
import cv2.cv as cv
#标记运动轨迹
'''
CalcOpticalFlowPyrLK 函数计算一个稀疏特征集的光流，使用金字塔中的迭代 Lucas-Kanade 方法
1 加载一段视频。
2 调用GoodFeaturesToTrack函数寻找兴趣点。
3 调用CalcOpticalFlowPyrLK函数计算出两帧图像中兴趣点的移动情况。
4 删除未移动的兴趣点。
5 在两次移动的点之间绘制一条线段。
'''
capture = cv.CaptureFromFile('../images/test.avi')

nbFrames = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_COUNT))
fps = cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FPS)
wait = 1#int (1/fps * 1000/1)
width = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH))
height = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT))

prev_gray = cv.CreateImage((width,height), 8, 1) #Will hold the frame at t-1
gray = cv.CreateImage((width,height), 8, 1) # Will hold the current frame

prevPyr = cv.CreateImage((height / 3, width + 8), 8, cv.CV_8UC1) #Will hold the pyr frame at t-1
currPyr = cv.CreateImage((height / 3, width + 8), 8, cv.CV_8UC1) # idem at t

max_count = 500
qLevel= 0.01
minDist = 10
prev_points = [] #Points at t-1
curr_points = [] #Points at t
lines=[] #To keep all the lines overtime

for f in xrange( nbFrames ):

    frame = cv.QueryFrame(capture) #Take a frame of the video

    cv.CvtColor(frame, gray, cv.CV_BGR2GRAY) #Convert to gray
    output = cv.CloneImage(frame)

    prev_points = cv.GoodFeaturesToTrack(gray, None, None, max_count, qLevel, minDist) #Find points on the image

    #Calculate the movement using the previous and the current frame using the previous points
    curr_points, status, err = cv.CalcOpticalFlowPyrLK(prev_gray, gray, prevPyr, currPyr, prev_points, (10, 10), 3, (cv.CV_TERMCRIT_ITER|cv.CV_TERMCRIT_EPS,20, 0.03), 0)


    #If points status are ok and distance not negligible keep the point
    k = 0
    for i in range(len(curr_points)):
        nb =  abs( int(prev_points[i][0])-int(curr_points[i][0]) ) + abs( int(prev_points[i][1])-int(curr_points[i][1]) )
        if status[i] and  nb > 2 :
            prev_points[k] = prev_points[i]
            curr_points[k] = curr_points[i]
            k += 1

    prev_points = prev_points[:k]
    curr_points = curr_points[:k]
    #At the end only interesting points are kept

    #Draw all the previously kept lines otherwise they would be lost the next frame
    for (pt1, pt2) in lines:
        cv.Line(frame, pt1, pt2, (255,255,255))

    #Draw the lines between each points at t-1 and t
    for prevpoint, point in zip(prev_points,curr_points):
        prevpoint = (int(prevpoint[0]),int(prevpoint[1]))
        cv.Circle(frame, prevpoint, 15, 0)
        point = (int(point[0]),int(point[1]))
        cv.Circle(frame, point, 3, 255)
        cv.Line(frame, prevpoint, point, (255,255,255))
        lines.append((prevpoint,point)) #Append current lines to the lines list


    cv.Copy(gray, prev_gray) #Put the current frame prev_gray
    prev_points = curr_points

    cv.ShowImage("The Video", frame)
    #cv.WriteFrame(writer, frame)
    cv.WaitKey(wait)