import serial
import numpy as np
import cv2

# Serial
ard = serial.Serial()
ard.port = "COM11"
ard.baudrate = 9600
ard.open()


class SerialCommunication:

    blank_image = np.zeros((720, 1280, 3), np.uint8)
    cv2.circle(blank_image, (640, 360), 200, (255, 255, 255), -1)
    laser_flag = False

    def move_motors(self, detection_boxes):

        for box in detection_boxes:

            # Box center
            x, y = self.get_box_center(box)

            # horizontal
            if x >= 740:
                print('R')
                ard.write('R'.encode())
            elif x <= 540:
                print('L')
                ard.write('L'.encode())

            # vertical
            if y >= 460:
                print('D')
                ard.write('D'.encode())
            elif y <= 260:
                print('U')
                ard.write('U'.encode())

    def laser(self, current_frame, detection_boxes):

        for box in detection_boxes:

            # Box center
            x, y = self.get_box_center(box)

            # Laser ON
            if (540 < x < 740) and (260 < y < 460):
                self.laser_flag = True

                cv2.addWeighted(current_frame, 0.7, self.blank_image, 0.3, 0, current_frame)
                cv2.putText(current_frame, "Laser ON", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)
                self.serial(self.laser_flag)
            else:
                self.laser_flag = False

                cv2.putText(current_frame, "Laser OFF", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)
                self.serial(self.laser_flag)

    def serial(self, laser_flag):

        if laser_flag:
            ard.write('S'.encode())
        else:
            ard.write('O'.encode())

    def get_box_center(self, box):
        x, y, w, h = box
        cx = x + w // 2
        cy = y + h // 2
        return cx, cy


