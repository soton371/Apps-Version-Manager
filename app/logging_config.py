from .config import settings
from icecream import ic


def logger(obj):
    if settings.env_mood == "local":
        ic(obj)


