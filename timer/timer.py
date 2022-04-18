import time
from datetime import datetime, timedelta 



class TimerResult:

    def __init__(self, function, *args, **kwargs):
        
        start_time = datetime.now()

        self.output = function(*args, **kwargs) 

        end_time = datetime.now()

        self.elapsed = end_time - start_time


def time(function, *args, **kwargs) -> TimerResult:
    
    return TimerResult(function, *args, **kwargs)
