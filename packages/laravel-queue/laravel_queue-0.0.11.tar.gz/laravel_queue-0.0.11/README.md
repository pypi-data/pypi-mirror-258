# Laravel Queue for Python

Currently:

- only supports reading
- only supports queues in postgres

### Create a Queue Object

```
from laravel-queue import Queue

connection_string = "postgresql://user:password@host:5432/db"
queue = Queue(connection_string)

```

#### Queue Args:
    connection: str or sqlalchemy.engine.base.Engine
    queue: str, default 'python', the queue name in the database
    jobs_table: str, default 'jobs.jobs', the table name for the jobs
    failed_jobs_table: str, default 'jobs.failed_jobs', the table name for the failed jobs


### Read Jobs from Queue
```
queue.read()  ## List of jobs returned, or:
jobs = queue.jobs  ## List of jobs in queue object
```

### Running Jobs
```
for job in queue.jobs:
    job.run(function, arg, kwarg=kwarg)  ## run any function and pass any args to it
```
function can be any function to run for this job
any args and kwargs will be used in this function

EX:
```
job.run(print, job.id)

Output: 12345
```

Jobs run in this way will be:
- removed from the jobs table and the queue object when complete (regardless of pass or fail)
- if failed, added to the failed jobs table along with the exception and a timestamp


### Managing Jobs Manually
For some reason, you may want to manage the job state yourself. (bypassing the run function above)

```
## Job failed
job.fail(exception) # Takes a string of the exception message, and fails the job. (both in the db and the queue)

## Job success
job.complete()  # Removes from job table and queue object
```