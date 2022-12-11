import enum

import cv2

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)


class Gender(enum.Enum):
    male = "male"
    female = "female"


class Recognizer:
    def __init__(self, face_net, gender_net):
        self.face_net = face_net
        self.gender_net = gender_net

    @staticmethod
    def highlight(net, frame, threshold=0.7):
        frameOpencvDnn = frame.copy()
        height = frameOpencvDnn.shape[0]
        width = frameOpencvDnn.shape[1]

        blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)

        net.setInput(blob)
        detections = net.forward()

        faceboxes = [
            [int(detections[0, 0, i, 3] * width),
             int(detections[0, 0, i, 4] * height),
             int(detections[0, 0, i, 5] * width),
             int(detections[0, 0, i, 6] * height)]

            for i in range(detections.shape[2]) if detections[0, 0, i, 2] > threshold
        ]
        return frameOpencvDnn, faceboxes

    def resolve(self, image):
        video = cv2.VideoCapture(image if image else 0)
        padding = 20

        while cv2.waitKey(1) < 0:
            hasFrame, frame = video.read()

            if not hasFrame:
                cv2.waitKey()
                break

            resultImg, faceboxes = self.highlight(self.face_net, frame)
            if not faceboxes:
                print("no face detected")

            genders = []
            for facebox in faceboxes:
                face = frame[
                       max(0, facebox[1] - padding): min(facebox[3] + padding, frame.shape[0] - 1),
                       max(0, facebox[0] - padding): min(facebox[2] + padding, frame.shape[1] - 1)
                       ]

                blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
                self.gender_net.setInput(blob)

                genders.append(
                    Gender.male if self.gender_net.forward()[0].argmax() == 0 else
                    Gender.female
                )
            return genders

    def recognize(self, image):
        return self.resolve(image)
