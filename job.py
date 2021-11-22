"""
    This scheduled job sending test stability report to specific api
"""

from apscheduler.schedulers.blocking import BlockingScheduler
from client.test_report_client import set_test_stability
sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=9)
def scheduled_job():
    """
    For changing job's cycle please change parameters
    :param day_of_week: Used for selecting work days
    :type arg: str
    :param `hour`: Used for selecting report hours
    :type arg: str
    """
    set_test_stability()

sched.start()
