from pathlib import Path

import aiofiles
import markovify
from aiogram import BaseMiddleware
from markovify import Text
from config import settings
from services.recognizer import Gender


class GeneratorMiddleware(BaseMiddleware):
    male_model: Text
    female_model: Text

    def __init__(self):
        super().__init__()
        models = []
        for phrase_file in (Path(settings.generator.phrases_dir) / "male").iterdir():
            with open(phrase_file) as f_male:
                models.append(Text(f_male.readlines()))
        self.male_model = markovify.combine(models).compile()
        models = []
        for phrase_file in (Path(settings.generator.phrases_dir) / "female").iterdir():
            with open(phrase_file) as f_female:
                models.append(Text(f_female.readlines()))
        self.female_model = markovify.combine(models).compile()

    def generate(self, gender: Gender):
        return self.male_model.make_sentence() if gender == Gender.male else self.female_model.make_sentence()

    async def __call__(self, handler, event, data):
        data["generator"] = self.generate
        return await handler(event, data)
