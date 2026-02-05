import cv2
import cv2
import numpy as np

prev_left_fit_average=prev_right_fit_average=None

def canny (image):
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(gray,(5,5),0)
    img_canny=cv2.Canny(blur,50,150)

    return img_canny

def region_of_interest(image):
    height,width=image.shape[:2]

    polygons = np.array([[
        (int(0.2 * width), int(height)),
        (int(0.45 * width), int(0.4 * height)),
        (int(0.55 * width), int(0.4* height)),
        (int(0.8 * width), int(height))
    ]], dtype=np.int32)
    mask=np.zeros((height,width), dtype=np.uint8)
    cv2.fillPoly(mask,polygons,255)
    masked_image=cv2.bitwise_and(image,mask)
    return masked_image

def make_cordinates(image,line_parameters):
    slope, intercept=line_parameters
    y1=image.shape[0]
    y2=int(y1*(3/5))
    if abs(slope) < 1e-6: #1e-6 é notação cientifica onde o que equivale a 1 * 10⁶,muito próximo de zero
        return None
    x1=int((y1-intercept)/slope)
    x2=int((y2-intercept)/slope)
    return np.array([x1,y1,x2,y2])

def average_slope_intercept(image,lines):
    global prev_left_fit_average,prev_right_fit_average

    left_fit=[]
    right_fit=[]


    if lines is None:
        return np.array([
            make_cordinates(image, prev_left_fit_average),
            make_cordinates(image, prev_right_fit_average)
        ])

    for line in lines:
        x1,y1,x2,y2=line.reshape(4)
        parameters=np.polyfit((x1,x2),(y1,y2),1)
        slope=parameters[0]
        interception=parameters[1]
        if slope<0:
            left_fit.append((slope,interception))
        else:
            right_fit.append((slope,interception))



    if len(left_fit) == 0 or len(right_fit) == 0:
        return np.array([
            make_cordinates(image, prev_left_fit_average),
            make_cordinates(image, prev_right_fit_average)
        ])

    left_fit_average=np.average(left_fit,axis=0)
    right_fit_average=np.average(right_fit,axis=0)
    print(left_fit_average,'left')
    print(right_fit_average,'right')
    try:
        left_line=make_cordinates(image,left_fit_average)
        right_line=make_cordinates(image,right_fit_average)

        prev_left_fit_average=left_fit_average
        prev_right_fit_average=right_fit_average

    except:
        left_line=make_cordinates(image,prev_left_fit_average)
        right_line=make_cordinates(image,prev_right_fit_average)

    return np.array([left_line,right_line])

def display_lines(image,lines):
    line_image=np.zeros_like(image)
    if lines is not None:
        for x1,y1,x2,y2 in lines :
            cv2.line(line_image,(x1,y1),(x2,y2),(255,0,255),12)
    return line_image

cap=cv2.VideoCapture('test_video.mp4')
while True:
    ret,frame=cap.read()
    if not ret:
        break
    canny_image=canny(frame)

    cropped_image=region_of_interest(canny_image)

    lines=cv2.HoughLinesP(cropped_image,2,np.pi/180,100,np.array([]),minLineLength=40,maxLineGap=5)

    averaged_lines=average_slope_intercept(frame,lines)



    line_image=display_lines(frame,averaged_lines)
    combo_image=cv2.addWeighted(frame,0.9,line_image,1,1)

    #desenho de faixa central ( solução inicial )
    x_left = averaged_lines[0][0]
    x_right = averaged_lines[1][0]

    x_left_2 = averaged_lines[0][2]
    x_rigth_2 = averaged_lines[1][2]

    x_center = int((x_right + x_left) / 2)
    x_center_top = int((x_rigth_2 + x_left_2) / 2)
    y = int(combo_image.shape[0])
    cv2.line(combo_image,(x_center,y),(x_center_top,int(y*3/5)),(255,255,0),12)

    cv2.imshow('result',combo_image)
    cv2.imshow('canny image',canny_image)
    cv2.imshow('roi',cropped_image)
    if cv2.waitKey(1) & 0xFF==27 : # aperte a tecla ESC para fechar abas
        break

cv2.destroyWindow()