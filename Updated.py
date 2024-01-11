#Works much better + you can avoid compiling two different files, here's the code:


import cv2 
import numpy as np

#define


def Transform4(image , lines):
    yellow_lane = []
    white_lane = []
    yellow_lane_averaged = None
    white_lane_averaged = None
    for line in lines:
      x1,y1,x2,y2 = line[0]

       #slope and intercept for interpolating

      temp = np.polyfit((x1 , x2) , (y1, y2) , 1)
      slope, intercept = temp

      if slope < 0:
         yellow_lane.append((slope, intercept))
      else:  
        white_lane.append((slope, intercept))

    if yellow_lane: 
         
      average1 = np.average(yellow_lane, axis = 0)

      slope , intercept = average1

      y1 = image.shape[0]
      y2 = int(y1*0.7)
      x1 = int((y1 - intercept)/slope)
      x2 = int((y2-intercept)/slope)

     # print(1)

      yellow_lane_averaged = np.array([x1 , y1 , x2 , y2])
    

    
    if white_lane:
       average2 = np.average(white_lane , axis = 0)
       #print(2)
       slope2 , intercept2 = average2

       y11 = image.shape[0]
       y22 = int(y11*0.7)
       x11 = int((y11 - intercept2)/slope2)
       x22 = int((y22-intercept2)/slope2)

       white_lane_averaged =  np.array([x11 , y11 , x22 , y22])
    

    if yellow_lane_averaged is None and white_lane_averaged is None:
        return None
    elif yellow_lane_averaged is None:
        return np.array([white_lane_averaged])
    elif white_lane_averaged is None:
        return np.array([yellow_lane_averaged])
    else:
        return np.array([yellow_lane_averaged, white_lane_averaged])






def Transform3 (image , lines):
    blank_line = np.zeros_like(image)

    if lines is not None:
        for line in lines:
            x1 , y1 , x2 , y2 = line.reshape(4)
            cv2.line(blank_line, (x1,y1) , (x2 , y2) , (0, 0 , 255) , 20)
     
    return blank_line





def Transform2 ( image ):
    #1670 , 950
    # 450 , 1530
    # 2700  1530
    # rem to use resized image bruh

    Defined_Region = np.array([[(1670, 950) , (450 , 1530) , (2700, 1530)]])

    all_black = np.zeros_like(image)

    cv2.fillPoly(all_black, Defined_Region , 255)

    #Rem you're taking the canny as input toh uspe bitwise AND krna h

    masked = cv2.bitwise_and(image , all_black)
    return masked



def Transform(image):
    Gaussian_frame = cv2.GaussianBlur(image , (5,5) , 0)

    gray_Frame = cv2.cvtColor(Gaussian_frame , cv2.COLOR_BGR2GRAY)

    canny_eff = cv2.Canny(gray_Frame , 150 , 150, apertureSize = 3)

    return canny_eff




Video_Given = cv2.VideoCapture('/Users/dazaiosamu/Downloads/Video1.mp4')


while True:

    junk1 , Frames = Video_Given.read()

    if Frames is None:
        break

    resized = cv2.resize(Frames, (2880 , 1624))

    Canny_frames = Transform(resized)

    RegionOfInterest = Transform2(Canny_frames)
    
    lines = cv2.HoughLinesP(RegionOfInterest , 1 , np.pi/180 , 100, minLineLength = 200, maxLineGap = 100)
    
    # Line_image = Transform3(resized , lines)

    #optimization to show better lines (thanks aditya bhaiya for hinting this kewk)
    
    optipmized_line = Transform4(resized , lines)

    Line_image = Transform3(resized , optipmized_line)

    final = cv2.addWeighted(Line_image , 0.7 , resized , 1 , 1)

    cv2.imshow('output' , final)
    if(cv2.waitKey(10) == ord('e')):
        break


cv2.waitKey()
cv2.destroyAllWindows()
cv2.waitKey(1)



