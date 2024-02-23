from dataclasses import dataclass
from uuid import uuid4, UUID
import phpserialize
import json
import warnings
from datetime import datetime


@dataclass
class Job:
    '''
        Job class to represent a job in the database queue
    '''
    id: int 
    uuid: UUID = uuid4()
    display_name: str = ''
    job: str = ''
    max_tries: int = None
    max_exceptions: int = None
    backoff: int = None
    timeout: int = None
    retry_until: int = None
    sentry_trace_parent_data: str = None
    command_name: str = None
    command: dict = None
    existing_job: bool = False
    raw_record: dict = None
    queue: any = None
    
    @classmethod
    def from_psycopg2(cls, record, queue=None):
        '''
            Creates a Job object from a record returned by psycopg2
        '''
        raw_record = record
        payload = json.loads(record[1])
        command = cls.__php_serialized_to_dict(payload['data']['command'])
        return cls(
            id=record[0],
            uuid=payload['uuid'],
            display_name=payload['displayName'],
            job=payload['job'],
            max_tries=payload['maxTries'],
            max_exceptions=payload['maxExceptions'],
            backoff=payload['backoff'],
            timeout=payload['timeout'],
            retry_until=payload['retryUntil'],
            command_name=payload['data']['commandName'],
            command=command,
            existing_job=True,
            raw_record=raw_record,
            queue=queue
        )
    @classmethod
    def __php_serialized_to_dict(cls, command: str) -> dict:
        command = phpserialize.loads(command.encode('utf-8'), object_hook=phpserialize.phpobject)
        command_dict = command._asdict()
        output = {
            key.decode(): val.decode() if isinstance(val, bytes) else val
            for key, val in command_dict.items()
        }
        return output
    
    def run(self, function:any, *args, **kwargs) -> bool:
        '''
            Runs the job
            function: any, the function to run
            *args: any, the arguments to pass to the function
            **kwargs: any, the keyword arguments to pass to the function

            Returns True if the job is successful, False if the job fails
            On fail, fails the job.
        '''
        try:
            function(*args, **kwargs)
            self.complete()
            return True
        except Exception as e:
            self.fail(str(e))
            return False
            
            
    
    def fail(self, exception: str):
        '''
            Fails the job, moving the record to the failed_jobs table and completing the job

            exception: str, the exception message to save in the failed_jobs table
        '''
        connection = self.queue.connection
        cursor = connection.cursor()
        insert = "INSERT INTO {} (connection, queue, payload, exception, failed_at) VALUES ('{}', '{}', '{}', '{}', '{}')".format(
            self.queue.failed_jobs_table,
            'database', 
            self.queue.queue, 
            self.raw_record[1], 
            exception, 
            datetime.now().isoformat()
        )
        cursor.execute(insert)
        connection.commit()
        cursor.close()
        self.complete()

    def complete(self):
        '''
            Completes the job
            Removes the job from the jobs table and the queue object
        '''
        connection = self.queue.connection
        cursor = connection.cursor()
        drop = "DELETE FROM {} WHERE id = {}".format(self.queue.jobs_table, self.id)
        cursor.execute(drop)
        connection.commit()
        cursor.close()
    
        self.queue.jobs.remove(self) 
    



class Queue:
    def __init__(self, connection: any, 
                 queue: str = 'python', 
                 jobs_table: str = 'jobs.jobs', 
                 failed_jobs_table: str = 'jobs.failed_jobs'):
        '''
        connection: str or sqlalchemy.engine.base.Engine
        queue: str, default 'python', the queue name in the database
        jobs_table: str, default 'jobs.jobs', the table name for the jobs
        failed_jobs_table: str, default 'jobs.failed_jobs', the table name for the failed jobs

        '''
        self.connection = self.__connect(connection)
        self.queue = queue
        self.jobs_table = jobs_table
        self.failed_jobs_table = failed_jobs_table
        self.jobs = []

    def read(self) -> list:
        '''
            Reads the jobs from the database queue
            returns a list of jobs
        '''
        cursor = self.connection.cursor()
        select = "SELECT id, payload FROM {} WHERE queue = '{}'".format(self.jobs_table, self.queue)
        cursor.execute(select)
        records = cursor.fetchall()
        cursor.close()
        if records:
            self.jobs = [Job.from_psycopg2(record, queue=self) for record in records]
        return self.jobs

    def dispatch(self, job: Job):
        '''
            Dispatches a job to the database queue
            @todo: Implement the dispatch method
        '''
        if job.__existing_job:
            raise ValueError('Job already exists in the database')  
        warnings.warn(
            'The dispatch method is not yet implemented. The job will not be dispatched to the queue.',
            UserWarning
        )



    def __connect(self, connection: any) -> any:
        if not isinstance(connection, str):
            connection = connection.url
        return self.__connect_with_psycopg2(connection)
        

    def __connect_with_psycopg2(self, connection_string: str):
        try:
            import psycopg2
        except ImportError:
            raise ImportError('psycopg2 is required by python-laravel-queue.')
        try:
            connection = psycopg2.connect(connection_string)
            return connection
        except:
            raise ValueError('Invalid connection string. Must be in the format: postgresql://user:password@host:5432/db')
    