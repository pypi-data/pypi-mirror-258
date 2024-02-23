# Laravel Queue for Python

Currently:

- only supports reading
- only supports queues in postgres

### Create a Queue Object

```
from laravel_queue import Queue

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
    job.run(function)  ## run any function and pass any args to it
```
function can be any function to run for this job
any parameters set in laravel will be passed to this function by name:
```
# laravel:
$this->groupId = 12;

# python
function(groupId = 12)
```

Jobs run in this way will be:
- removed from the jobs table and the queue object when complete (regardless of pass or fail)
- if failed, added to the failed jobs table along with the exception and a timestamp


Additionally, you can specify a `cache_lock_uid`
This can be either a str or a list of strings.
This is to be used for managing the job cache if you are using the `ShouldBeUnique` or `ShouldBeUniqueUntilProcessing` properties in Laravel
The `cache_lock_uid` should resemble what you have set `uniqueId()` to in laravel.
If a list is sent, you can specify parameters to be filled with `$`:

```
# Laravel:
$this->param1 = 1
$this->param2 = 2

public function uniqueId(): string
    {
        return $this->param1 . '-' . $this->param2;
    }


# Python
job.run(function_name, cache_lock_uid = ['$param1', '-', '$param2'])

## $param1 and $param2 will be swapped in with the cooresponding value.

```




### Managing Jobs Manually
For some reason, you may want to manage the job state yourself. (bypassing the run function above)

```
## Job proccessing  (When you have unique jobs happening on the queue)
job.release_lock(cache_uid) # Takes a string of the uid used in the laravel job


## Job failed
job.fail(exception) # Takes a string of the exception message, and fails the job. (both in the db and the queue)

## Job success
job.complete()  # Removes from job table and queue object
```