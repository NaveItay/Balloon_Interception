# Balloon Interception System
### Deep Learning, Computer Vision, and Robotics.

![title](/github_images/Balloon_Interception.PNG)
[![title](/github_images/youtube.png "Balloon Interception - Deep Learning, Computer Vision, and Robotics")](https://youtu.be/KMWxmcNWnjA)

### Project steps:

1. Circuit diagram and hardware
2. Data labeling
3. Training CNN model (Darknet framework)
4. Code                
   - Initialize Model
   - Balloon Detection
   - Draw Detections
   - Object Tracking Camera
   - Laser Balloon Interception

# 
###### Circuit Diagram and Hardware
>
>  ![alt text](/github_images/Schematic.png)
>

>  ##### Controllable Electric Tilt Two-Degree-Of-Freedom Manipulator Horizontal And Vertical Rotation
> ![alt text](/github_images/Controllable_Electric_Tilt_Two_Degree_Of_Freedom_Manipulator_Horizontal_And_Vertical_Rotation.PNG)
> 
>  - Digital Coreless Servo, 360 degrees for horizontal axis     
>  - Digital Coreless Servo, 180 degrees for vertical axis
>

>  #####  Blue Laser Pointer 445nm 5000m 2W Laser Light
> ![alt text](/github_images/laser.PNG)
>
>  - Wavelength 445nm
>  - Safety level: Class IV
>  - Max brightness: > 350lm/500lm/1000lm
>  - Circuit control: APC
>  - Dimension: φ40*190mm 
>  - Beam style: continuous line
>

>  ##### PC (Ubuntu linux)
>  CUDA technology support with NVIDIA® GeForce® RTX 2080 Ti graphics card.
>

<p>
<br />
<br />
</p>

###### Data labeling
> ![alt text](/github_images/Label.PNG)
> The dataset contains about 1000 labeled images, a free dataset downloaded from [googleapis.com](https://storage.googleapis.com/openimages/web/index.html).
>

<p>
<br />
<br />
</p>

###### YOLOv4-tiny Convolutional Neural Network
> ![alt text](/github_images/yolov4_architecture.PNG)
> 
> YOLO uses a totally different approach than other previous detection systems. It applies a single neural network to the full image.
> This network divides the image into regions and predicts bounding boxes and probabilities for each region.
> These bounding boxes are weighted by the predicted probabilities.
> The basic idea of YOLO is exhibited in the figure below.
> 
> YOLO divides the input image into an S × S grid and each grid cell is responsible for predicting the object centered
> in that grid cell.

<p>
<br />
<br />
</p>

###### Code
> 
> ##### Initialize Model
>  ```
>      def initialize_model(self):
>
>        with open('./model/Balloon_interception.names', 'r') as f:
>            self.class_names = [cname.strip() for cname in f.readlines()]
>
>        net = cv2.dnn.readNet('./model/Balloon_interception.weights', './model/Balloon_interception.cfg')
>        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
>        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
>        self.model = cv2.dnn_DetectionModel(net)
>        self.model.setInputParams(1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)
>  ```
>  
> ##### Balloon Detection
>  ```
>          self.classes, scores, boxes = self.model.detect(frame, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
>  ```
>
>  ##### Draw Detections
>  ```
>      def draw_objects(self, frame, classes, scores, boxes):
>
>        for (class_id, score, box) in zip(classes, scores, boxes):
>
>            # Box center
>            x, y = self.get_box_center(box)
>
>            label = "(%d, %d)" % (x, y)
>            overlay = frame.copy()
>
>            # Draw Balloon
>            if class_id[0] == 0:
>                cv2.circle(overlay, (x, y), int(box[3] / 2), COLORS[1], 2)
>                cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
>                cv2.putText(frame, label + " " + str(score), (box[0], box[1] - 10),
>                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
>
>        return frame
>
>    def get_box_center(self, box):
>        x, y, w, h = box
>        cx = x + x + w // 2
>        cy = y + y + h // 2
>        return cx, cy
>  ```
>  
>  ##### Object Tracking Camera
>  ```
>  ![alt text](/github_images/logic_explain.PNG)
> 
>     def move_motors(self, detection_boxes):
>
>        for box in detection_boxes:
>
>            # Box center
>            x, y = self.get_box_center(box)
>
>            # horizontal
>            if x >= 740:
>                print('R')
>                ard.write('R'.encode())
>            elif x <= 540:
>                print('L')
>                ard.write('L'.encode())
>
>            # vertical
>            if y >= 460:
>                print('D')
>                ard.write('D'.encode())
>            elif y <= 260:
>                print('U')
>                ard.write('U'.encode())
>  ```
>
>  ##### Laser Balloon Interception
>  ```
>      def laser(self, current_frame, detection_boxes):
>
>        for box in detection_boxes:
>
>            # Box center
>            x, y = self.get_box_center(box)
>
>            # Laser ON
>            if (540 < x < 740) and (260 < y < 460):
>                self.laser_flag = True
>
>                cv2.addWeighted(current_frame, 0.7, self.blank_image, 0.3, 0, current_frame)
>                cv2.putText(current_frame, "Laser ON", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)
>                self.serial(self.laser_flag)
>            else:
>                self.laser_flag = False
>
>                cv2.putText(current_frame, "Laser OFF", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)
>                self.serial(self.laser_flag)
>
>    def serial(self, laser_flag):
>
>        if laser_flag:
>            ard.write('S'.encode())
>        else:
>            ard.write('O'.encode())
> ```
> 
