from typing import Any, Union, Dict

from aiogram.dispatcher.filters import BaseFilter


class GenderFilter(BaseFilter):
    async def __call__(self, *args: Any, **kwargs: Any) -> Union[bool, Dict[str, Any]]:
        