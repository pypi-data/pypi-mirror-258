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
    
    @classmethod
    def from_psycopg2(cls, record):
        '''
            Creates a Job object from a record returned by psycopg2
        '''
        raw_record = record
        payload = json.loads(record[0])
        command = cls.__php_serialized_to_dict(payload['data']['command'])
        return cls(
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
            raw_record=__raw_record
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
        self.payload_column = 'payload'

    def read(self) :
        '''
            Reads the jobs from the database queue
        '''
        cursor = self.connection.cursor()
        select = "SELECT {} FROM {} WHERE queue = '{}'".format(self.payload_column, self.jobs_table, self.queue)
        cursor.execute(select)
        records = cursor.fetchall()
        cursor.close()
        if records:
            return [Job.from_psycopg2(record) for record in records]
        return None

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

    def fail_job(self, job: Job):
        '''
            Fails a job in the database queue
        '''
        job = self.__get_job_from_db(job.uuid)
        if not job:
            raise ValueError('Job does not exist in the database')
        
        self.__fail_job_in_db(job)


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
    
    def __get_job_from_db(self, uuid: UUID):
        '''
            Gets the job from the database
        '''
        cursor = self.connection.cursor()
        select = "SELECT * FROM {} WHERE uuid = '{}'".format(self.payload_column, self.jobs_table, uuid)
        cursor.execute(select)
        record = cursor.fetchone()
        cursor.close()
        if record:
            return Job.from_psycopg2(record)
        return None

    def __fail_job_in_db(self, job:Job, exception: str = None):
        '''
            Fails a job in the database
        '''
        cursor = self.connection.cursor()
        insert = "INSERT INTO {} (connection, queue, payload, exception, failed_at) VALUES ('{}', '{}', '{}', '{}', '{}')".format(
            self.failed_jobs_table,
            'database', 
            self.queue, 
            job.__raw_record[3], 
            exception, 
            datetime.now().isoformat()
        )
        cursor.execute(insert)
        self.connection.commit()
        cursor.close()
