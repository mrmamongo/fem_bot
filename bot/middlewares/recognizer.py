from pathlib import Path
from typing import Any

import cv2
from aiogram import BaseMiddleware

from bot.config import settings
from bot.services.recognizer import Recognizer


class RecognizerMiddleware(BaseMiddleware):
    face_net: Any
    gender_net: Any

    def __init__(self):
        super().__init__()
        model_path = Path(settings.recognizer.model_dir)
        # self.face_net = cv2.dnn.readNet(
        #     model_path / "opencv_face_detector_uint8.pb",
        #     model_path / "opencv_face_detector.pbtxt",
        # )
        gender_proto = model_path / "gender_deploy.prototxt"
        gender_caffe = model_path / "gender_net.caffemodel"
        self.gender_net = cv2.dnn.readNetFromCaffe(gender_proto, gender_caffe)

    async def __call__(self, handler, event, data):
        data["recognizer"] = Recognizer(self.face_net, self.gender_net)
        return await handler(event, data)
