import cv2 
import numpy as np

if false:
 def exact(image , line_parameters):
     slope ,intercept = line_parameters
     y1 = image.shape[0]
     y2 = int(y1*0.7)
     x1 = int((y1 - intercept)/slope)
     x2 = int((y2 - intercept)/slope)

     return np.array([x1, y1 , x2 , y2])



 def Transform4(image , lines):
     white_lane = []
     yellow_lane = []
     if lines is not None:
       for line in lines:
         x1,y1,x2,y2 = line.reshape(4)

         #slope and intercept for interpolating

         temp = (np.polyfit((x1 , y1) , (x2, y2) , 1))
         slope = temp[0]
         intercept = temp[1]

         if slope < 0:
             yellow_lane.append((slope, intercept))
         else:
             white_lane.append((slope, intercept))


     average1 = np.average(yellow_lane, axis = 0)
     average2 = np.average(white_lane , axis = 0)

     yellow_lane_averaged = exact(image , average1)
     white_lane_averaged = exact(image , average2)
       

     return np.array([yellow_lane_averaged , white_lane_averaged])







def Transform3 (image , lines):
    blank_line = np.zeros_like(image)

    if lines is not None:
        for line in lines:
            x1 , y1 , x2 , y2 = line[0]
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

