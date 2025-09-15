from .sync import JournalApi
from .async_ import AsyncJournalApi

__all__ = ["JournalApi", "AsyncJournalApi"]


class OmniApi():
    def __init__(self, cookie):
        self.cookie = cookie

    def get_rooms(self): # TODO
        pass

    def get_schedule(self): # TODO
        pass
