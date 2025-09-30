from core.datatypes.timestamp import Timestamp

import datetime

class DT:

    @staticmethod
    def now():
        return Timestamp(
            datetime.datetime.now()
            , tz='US/Pacific'
        )
