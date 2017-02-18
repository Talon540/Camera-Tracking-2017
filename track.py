import cv2
from networktables import NetworkTables
from grip import GripPipeline

def extra_processing(pipeline):
    center_x = []
    center_y = []
    widths =[]
    heights = []
    align = 0

    for contour in pipeline.filter_contours_output:
        #Determines the bounding boxes around the target contours
        #It then determines the coordinates at the top left of the box
        x, y, w, h = cv2.boundingRect(contour)
        center_x.append(x + w / 2)
        center_y.append(y + h / 2)
        widths.append(w)
        heights.append(h)
        
        #Finds the centerX values if the value of the Array is not 0
        if len(center_x) > 0:
            #Takes the first value of the array
            cX = center_x.pop(0)
            if (cX <= 310 and cX >= 210):
                #0 = Aligned
                align = 0
                print (align)
            elif (cX >= 311):
                #-1 = Too Left
                align = -1
                print(align)
            elif (cX <= 100):
                #1 = Too Right
                align = 1
                print(align)

        #Calculates area
        #Tests for Dummy Steamworks Goal from 12/14 ft gave an area ~ 400 square px
        raw_area = [a*b for a,b in zip(widths, heights)]
        area = raw_area.pop(0)
        print (area)

        #Sends Data to Network Table
        table = NetworkTables.getTable("peg")
        table.putNumber("area", area)
        table.putNumber("align", align)

        
def main():
    #Establishes a connection to NetworkTable
    print("Establishing a connection to the NetworkTable")
    NetworkTables.setClientMode()
    NetworkTables.setIPAddress("roboRIO-540-frc.local")
    NetworkTables.initialize()
    print("Connected to NetworkTable")

    #Captures frames and runs them through the GRIP Pipeline
    print("Starting vision tracking and GRIP Pipeline")
    cp = cv2.VideoCapture(0)
    pipeline = GripPipeline()
    while cp.isOpened():
        have_frame, frame = cp.read()
        if have_frame:
            pipeline.process(frame)
            extra_processing(pipeline)

if __name__ == '__main__':
    main()
