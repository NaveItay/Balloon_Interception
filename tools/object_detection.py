import cv2

CONFIDENCE_THRESHOLD = 0.6
NMS_THRESHOLD = 0.1
COLORS = [(255, 0, 0), (0, 0, 255), (195, 195, 195), (0, 255, 0)]


class ObjectDetection:
    class_names = []
    model = None

    def initialize_model(self):

        with open('./model/Balloon_interception.names', 'r') as f:
            self.class_names = [cname.strip() for cname in f.readlines()]

        net = cv2.dnn.readNet('./model/Balloon_interception.weights', './model/Balloon_interception.cfg')
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        self.model = cv2.dnn_DetectionModel(net)
        self.model.setInputParams(1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)

    def detect(self, frame):

        self.classes, scores, boxes = self.model.detect(frame, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)

        return self.classes, scores, boxes

    def draw_objects(self, frame, classes, scores, boxes):

        for (class_id, score, box) in zip(classes, scores, boxes):

            # Box center
            x, y = self.get_box_center(box)

            label = "(%d, %d)" % (x, y)
            overlay = frame.copy()

            # Draw Balloon
            if class_id[0] == 0:
                cv2.circle(overlay, (x, y), int(box[3] / 2), COLORS[1], 2)
                cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
                cv2.putText(frame, label + " " + str(score), (box[0], box[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return frame

    def get_box_center(self, box):
        x, y, w, h = box
        cx = x + w // 2
        cy = y + h // 2
        return cx, cy
