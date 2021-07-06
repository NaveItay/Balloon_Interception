import cv2
from tools.object_detection import ObjectDetection
from tools.serial import SerialCommunication

o_detection = ObjectDetection()
o_detection.initialize_model()
serial = SerialCommunication()

# Load video
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while cap.isOpened():

    _, current_frame = cap.read()

    # Flip horizontal
    current_frame = cv2.flip(current_frame, 0)

    # Detect balloon
    classes, scores, detection_boxes = o_detection.detect(current_frame)

    # Draw balloon
    current_frame = o_detection.draw_objects(current_frame, classes, scores, detection_boxes)

    # Motors tracker
    serial.move_motors(detection_boxes)

    # Shoot laser
    serial.laser(current_frame, detection_boxes)

    cv2.imshow("Image", current_frame)
    cv2.waitKey(1)

# shut down capture system
cap.release()
