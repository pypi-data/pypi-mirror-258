import logging,re,time
from threading import Thread
from crontab import CronTab
from localstack.utils.scheduler import ScheduledTask,Scheduler
from snowflake_local.engine.models import Query
from snowflake_local.engine.queries import execute_query
from snowflake_local.tasks.models import Task
LOG=logging.getLogger(__name__)
class TaskExecutor(ScheduledTask):
	task_obj:0
	def __init__(A,task):A.task_obj=task;super().__init__(A.run_task);A.period=True
	def run_task(A):
		try:B=Query(query=A.task_obj.definition);C=execute_query(B);LOG.debug('Result returned from executing task %s: %s',A.task_obj.name,C)
		except Exception as D:LOG.info('Error executing task %s: %s',A.task_obj.name,D)
	def set_next_deadline(B):
		A=str(B.task_obj.schedule);C=re.match('\\s*(\\d+)\\s+MINUTE',A,flags=re.I);D=re.match('\\s*USING\\s+CRON((\\s+\\S+){5}).*',A,flags=re.I)
		if C:E=int(C.group(1))*60
		elif D:F=CronTab(D.group(1).strip());E=F.next()
		else:LOG.info('Unsupported task schedule expression: %s',A);return
		B.deadline=time.time()+E
class TaskScheduler:
	scheduler:0
	def __init__(A):A.scheduler=Scheduler();A.thread=None
	def schedule_task(A,task):A._start();B=TaskExecutor(task);B.set_next_deadline();A.scheduler.add(B)
	def _start(A):
		if not A.thread:A.thread=Thread(target=A.scheduler.run,name='snowflake-scheduler');A.thread.start()
SCHEDULER=TaskScheduler()