import cv2
import numpy as np
import define.py
#IMPORTANT
#PRESS 'x' TO DESTROY WINDOW

#Give path of your video1 included here ig?

Video_Given = cv2.VideoCapture('/path/to/yout/Video.mp4')


while True:

    junk1 , Frames = Video_Given.read()

    if Frames is None:
        break

    resized = cv2.resize(Frames, (2880 , 1624))

    Canny_frames = Transform(resized)

    RegionOfInterest = Transform2(Canny_frames)
    
    lines = cv2.HoughLinesP(RegionOfInterest , 1 , np.pi/180 , 100, minLineLength = 200, maxLineGap = 100)
    
    Line_image = Transform3(resized , lines)

    
    
    #optipmized_line = Transform4(resized , lines)

    final = cv2.addWeighted(Line_image , 0.9 , resized , 1 , 1)

    cv2.imshow('output' , final)
    if(cv2.waitKey(10) == ord('x')):
        break

#PRESS 'x' TO DESTROY WINDOW
cv2.waitKey()
cv2.destroyAllWindows()
cv2.waitKey(1)
