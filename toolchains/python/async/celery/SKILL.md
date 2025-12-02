---
name: celery
description: Distributed task queue system for Python enabling asynchronous execution of background jobs, scheduled tasks, and workflows across multiple workers with Django, Flask, and FastAPI integration.
progressive_disclosure:
  entry_point:
    - summary
    - when_to_use
    - quick_start
  sections:
    - core_concepts
    - broker_setup
    - task_basics
    - task_execution
    - task_routing
    - periodic_tasks
    - workflows
    - error_handling
    - monitoring
    - framework_integration
    - testing
    - production_patterns
    - performance
    - use_cases
    - alternatives
    - best_practices
    - troubleshooting
---

# Celery: Distributed Task Queue

## Summary
Celery is a distributed task queue system for Python that enables asynchronous execution of background jobs across multiple workers. It supports scheduling, retries, task workflows, and integrates seamlessly with Django, Flask, and FastAPI.

## When to Use
- **Background Processing**: Offload long-running operations (email, file processing, reports)
- **Scheduled Tasks**: Cron-like periodic jobs (cleanup, backups, data sync)
- **Distributed Computing**: Process tasks across multiple workers/servers
- **Async Workflows**: Chain, group, and orchestrate complex task dependencies
- **Real-time Processing**: Handle webhooks, notifications, data pipelines
- **Load Balancing**: Distribute CPU-intensive work across workers

**Don't Use When**:
- Simple async I/O (use `asyncio` instead)
- Real-time request/response (use async web frameworks)
- Sub-second latency required (use in-memory queues)
- Minimal infrastructure (use simpler alternatives like RQ or Huey)

## Quick Start

### Installation
```bash
# Basic installation
pip install celery

# With Redis broker
pip install celery[redis]

# With RabbitMQ broker
pip install celery[amqp]

# Full batteries (recommended)
pip install celery[redis,msgpack,auth,cassandra,elasticsearch,s3,sqs]
```

### Basic Setup
```python
# celery_app.py
from celery import Celery

# Create Celery app with Redis broker
app = Celery(
    'myapp',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1'
)

# Configuration
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# Define a task
@app.task
def add(x, y):
    return x + y

@app.task
def send_email(to, subject, body):
    # Simulate email sending
    import time
    time.sleep(2)
    print(f"Email sent to {to}: {subject}")
    return {"status": "sent", "to": to}
```

### Running Workers
```bash
# Start worker
celery -A celery_app worker --loglevel=info

# Multiple workers with concurrency
celery -A celery_app worker --concurrency=4 --loglevel=info

# Named worker for specific queues
celery -A celery_app worker -Q emails,reports --loglevel=info
```

### Executing Tasks
```python
# Call task asynchronously
result = add.delay(4, 6)

# Wait for result
print(result.get(timeout=10))  # 10

# Apply async with options
result = send_email.apply_async(
    args=['user@example.com', 'Hello', 'Welcome!'],
    countdown=60  # Execute after 60 seconds
)

# Check task state
print(result.status)  # PENDING, STARTED, SUCCESS, FAILURE
```

---

## Core Concepts

### Architecture Components

**Broker**: Message queue that stores tasks
- Redis (recommended for most use cases)
- RabbitMQ (enterprise-grade, complex)
- Amazon SQS (serverless, AWS-native)

**Workers**: Processes that execute tasks
- Pull tasks from broker
- Execute task code
- Store results in backend

**Result Backend**: Storage for task results
- Redis (fast, in-memory)
- Database (PostgreSQL, MySQL)
- S3 (large results)
- Cassandra, Elasticsearch (specialized)

**Beat Scheduler**: Periodic task scheduler
- Cron-like scheduling
- Interval-based tasks
- Stores schedule in database or file

### Task States
```
PENDING → STARTED → SUCCESS
                 → RETRY → SUCCESS
                 → FAILURE
```

- **PENDING**: Task waiting in queue
- **STARTED**: Worker picked up task
- **SUCCESS**: Task completed successfully
- **FAILURE**: Task raised exception
- **RETRY**: Task will retry after failure
- **REVOKED**: Task cancelled before execution

---

## Broker Setup

### Redis Configuration
```python
# celery_config.py
broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/1'

# With authentication
broker_url = 'redis://:password@localhost:6379/0'

# Redis Sentinel (high availability)
broker_url = 'sentinel://localhost:26379;sentinel://localhost:26380'
broker_transport_options = {
    'master_name': 'mymaster',
    'sentinel_kwargs': {'password': 'password'},
}

# Redis connection pool settings
broker_pool_limit = 10
broker_connection_retry = True
broker_connection_retry_on_startup = True
broker_connection_max_retries = 10
```

### RabbitMQ Configuration
```python
# Basic RabbitMQ
broker_url = 'amqp://guest:guest@localhost:5672//'

# With virtual host
broker_url = 'amqp://user:password@localhost:5672/myvhost'

# High availability (multiple brokers)
broker_url = [
    'amqp://user:password@host1:5672//',
    'amqp://user:password@host2:5672//',
]

# RabbitMQ-specific settings
broker_heartbeat = 30
broker_pool_limit = 10
```

### Amazon SQS Configuration
```python
# AWS SQS (serverless)
broker_url = 'sqs://'
broker_transport_options = {
    'region': 'us-east-1',
    'queue_name_prefix': 'myapp-',
    'visibility_timeout': 3600,
    'polling_interval': 1,
}

# With custom credentials
import boto3
broker_transport_options = {
    'region': 'us-east-1',
    'predefined_queues': {
        'default': {
            'url': 'https://sqs.us-east-1.amazonaws.com/123456789/myapp-default',
        }
    }
}
```

---

## Task Basics

### Task Definition
```python
from celery import Task, shared_task
from celery_app import app

# Method 1: Decorator
@app.task
def simple_task(x, y):
    return x + y

# Method 2: Shared task (framework-agnostic)
@shared_task
def framework_task(data):
    return process(data)

# Method 3: Task class (advanced)
class CustomTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        print(f"Task {task_id} succeeded with {retval}")

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print(f"Task {task_id} failed: {exc}")

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        print(f"Task {task_id} retrying: {exc}")

@app.task(base=CustomTask)
def monitored_task(x):
    return x * 2
```

### Task Options
```python
@app.task(
    name='custom.task.name',           # Custom task name
    bind=True,                          # Bind task instance as first arg
    ignore_result=True,                 # Don't store result (performance)
    max_retries=3,                      # Max retry attempts
    default_retry_delay=60,             # Retry delay in seconds
    rate_limit='100/h',                 # Rate limiting
    time_limit=300,                     # Hard time limit (kills task)
    soft_time_limit=240,                # Soft time limit (raises exception)
    serializer='json',                  # Task serializer
    compression='gzip',                 # Compress large messages
    priority=5,                         # Task priority (0-9)
    queue='high_priority',              # Target queue
    routing_key='priority.high',        # Routing key
    acks_late=True,                     # Acknowledge after execution
    reject_on_worker_lost=True,         # Reject if worker dies
)
def advanced_task(self, data):
    try:
        return process(data)
    except Exception as exc:
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)
```

### Task Context (bind=True)
```python
@app.task(bind=True)
def context_aware_task(self, x, y):
    # Access task metadata
    print(f"Task ID: {self.request.id}")
    print(f"Task Name: {self.name}")
    print(f"Args: {self.request.args}")
    print(f"Kwargs: {self.request.kwargs}")
    print(f"Retries: {self.request.retries}")
    print(f"Delivery Info: {self.request.delivery_info}")

    # Manual retry
    try:
        result = risky_operation(x, y)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60, max_retries=3)

    return result
```

---

## Task Execution

### Delay vs Apply Async
```python
# delay() - Simple async execution
result = add.delay(4, 6)

# apply_async() - Full control
result = add.apply_async(
    args=(4, 6),
    kwargs={'extra': 'data'},

    # Timing options
    countdown=60,                    # Execute after N seconds
    eta=datetime(2025, 12, 1, 10, 0),  # Execute at specific time
    expires=3600,                    # Task expires after N seconds

    # Routing options
    queue='math',                    # Target specific queue
    routing_key='math.add',          # Custom routing key
    exchange='tasks',                # Target exchange
    priority=9,                      # High priority

    # Execution options
    serializer='json',               # Message serializer
    compression='gzip',              # Compress payload
    retry=True,                      # Auto-retry on failure
    retry_policy={
        'max_retries': 3,
        'interval_start': 0,
        'interval_step': 0.2,
        'interval_max': 0.2,
    },

    # Task linking
    link=log_result.s(),             # Success callback
    link_error=handle_error.s(),     # Error callback
)

# Check result
if result.ready():
    print(result.get())  # Get result (blocks)
    print(result.result)  # Get result (non-blocking)
```

### Task Signatures
```python
from celery import signature

# Create signature (doesn't execute)
sig = add.signature((2, 2), countdown=10)
sig = add.s(2, 2)  # Shorthand

# Partial arguments (currying)
partial = add.s(2)  # One arg fixed
result = partial.apply_async(args=(4,))  # Add second arg

# Immutable signature (args can't be replaced)
immutable = add.si(2, 2)

# Clone and modify
new_sig = sig.clone(countdown=60)

# Execute signature
result = sig.delay()
result = sig.apply_async()
result = sig()  # Synchronous execution
```

### Result Handling
```python
# Basic result retrieval
result = add.delay(4, 6)
value = result.get(timeout=10)  # Blocks until complete

# Non-blocking result check
if result.ready():
    print(result.result)

# Result states
print(result.status)      # PENDING, STARTED, SUCCESS, FAILURE
print(result.successful())  # True if SUCCESS
print(result.failed())      # True if FAILURE

# Result metadata
print(result.traceback)   # Exception traceback if failed
print(result.info)        # Task return value or exception

# Forget result (free memory)
result.forget()

# Revoke task (cancel)
result.revoke(terminate=True)  # Kill running task
add.AsyncResult(task_id).revoke()  # Revoke by ID
```

---

## Task Routing

### Queue Configuration
```python
# Define queues
from kombu import Queue, Exchange

app.conf.task_queues = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('high_priority', Exchange('priority'), routing_key='priority.high'),
    Queue('low_priority', Exchange('priority'), routing_key='priority.low'),
    Queue('emails', Exchange('tasks'), routing_key='tasks.email'),
    Queue('reports', Exchange('tasks'), routing_key='tasks.report'),
)

# Default queue
app.conf.task_default_queue = 'default'
app.conf.task_default_exchange = 'tasks'
app.conf.task_default_routing_key = 'default'
```

### Task Routing Rules
```python
# Route specific tasks to queues
app.conf.task_routes = {
    'myapp.tasks.send_email': {'queue': 'emails'},
    'myapp.tasks.generate_report': {'queue': 'reports', 'priority': 9},
    'myapp.tasks.*': {'queue': 'default'},
}

# Function-based routing
def route_task(name, args, kwargs, options, task=None, **kw):
    if 'email' in name:
        return {'queue': 'emails', 'routing_key': 'email.send'}
    elif 'report' in name:
        return {'queue': 'reports', 'priority': 5}
    return {'queue': 'default'}

app.conf.task_routes = (route_task,)
```

### Worker Queue Binding
```bash
# Worker consuming specific queues
celery -A myapp worker -Q emails,reports --loglevel=info

# Multiple workers for different queues
celery -A myapp worker -Q high_priority -c 4 --loglevel=info
celery -A myapp worker -Q default -c 2 --loglevel=info
celery -A myapp worker -Q low_priority -c 1 --loglevel=info
```

### Priority Queues
```python
# Configure priority support
app.conf.task_queue_max_priority = 10
app.conf.task_default_priority = 5

# Send task with priority
high_priority_task.apply_async(args=(), priority=9)
low_priority_task.apply_async(args=(), priority=1)

# Priority-based routing
app.conf.task_routes = {
    'critical_task': {'queue': 'default', 'priority': 10},
    'background_task': {'queue': 'default', 'priority': 1},
}
```

---

## Periodic Tasks

### Celery Beat Setup
```python
# celery_config.py
from celery.schedules import crontab, solar

# Periodic task schedule
beat_schedule = {
    # Run every 30 seconds
    'add-every-30-seconds': {
        'task': 'myapp.tasks.add',
        'schedule': 30.0,
        'args': (16, 16)
    },

    # Run every morning at 7:30 AM
    'send-daily-report': {
        'task': 'myapp.tasks.send_daily_report',
        'schedule': crontab(hour=7, minute=30),
    },

    # Run every Monday morning
    'weekly-cleanup': {
        'task': 'myapp.tasks.cleanup',
        'schedule': crontab(hour=0, minute=0, day_of_week=1),
    },

    # Run on specific days
    'monthly-report': {
        'task': 'myapp.tasks.monthly_report',
        'schedule': crontab(hour=0, minute=0, day_of_month='1'),
        'kwargs': {'month_offset': 1}
    },

    # Solar schedule (sunrise/sunset)
    'wake-up-at-sunrise': {
        'task': 'myapp.tasks.morning_routine',
        'schedule': solar('sunrise', -37.81, 144.96),  # Melbourne
    },
}

app.conf.beat_schedule = beat_schedule
```

### Crontab Patterns
```python
from celery.schedules import crontab

# Every minute
crontab()

# Every 15 minutes
crontab(minute='*/15')

# Every hour at :30
crontab(minute=30)

# Every day at midnight
crontab(hour=0, minute=0)

# Every weekday at 5 PM
crontab(hour=17, minute=0, day_of_week='1-5')

# Every Monday, Wednesday, Friday at noon
crontab(hour=12, minute=0, day_of_week='mon,wed,fri')

# First day of month
crontab(hour=0, minute=0, day_of_month='1')

# Last day of month (use day_of_month='28-31' with logic in task)
crontab(hour=0, minute=0, day_of_month='28-31')

# Quarterly (every 3 months)
crontab(hour=0, minute=0, day_of_month='1', month_of_year='*/3')
```

### Running Beat Scheduler
```bash
# Start beat scheduler
celery -A myapp beat --loglevel=info

# Beat with custom scheduler
celery -A myapp beat --scheduler django_celery_beat.schedulers:DatabaseScheduler

# Combine worker and beat (development only)
celery -A myapp worker --beat --loglevel=info
```

### Dynamic Schedules (django-celery-beat)
```bash
pip install django-celery-beat
```

```python
# settings.py (Django)
INSTALLED_APPS = [
    'django_celery_beat',
]

# Migrate database
python manage.py migrate django_celery_beat

# Run beat with database scheduler
celery -A myapp beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

```python
# Create periodic task via Django admin or ORM
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule
import json

# Create interval schedule (every 10 seconds)
schedule, created = IntervalSchedule.objects.get_or_create(
    every=10,
    period=IntervalSchedule.SECONDS,
)

PeriodicTask.objects.create(
    interval=schedule,
    name='Import feed every 10 seconds',
    task='myapp.tasks.import_feed',
    args=json.dumps(['https://example.com/feed']),
)

# Create crontab schedule
schedule, created = CrontabSchedule.objects.get_or_create(
    minute='0',
    hour='*/4',  # Every 4 hours
    day_of_week='*',
    day_of_month='*',
    month_of_year='*',
)

PeriodicTask.objects.create(
    crontab=schedule,
    name='Hourly cleanup',
    task='myapp.tasks.cleanup',
)
```

---

## Workflows (Canvas)

### Chains
```python
from celery import chain

# Sequential execution
result = chain(add.s(2, 2), add.s(4), add.s(8))()
# Equivalent to: add(add(add(2, 2), 4), 8)
# Result: 16

# Shorthand syntax
result = (add.s(2, 2) | add.s(4) | add.s(8))()

# Chain with different tasks
workflow = (
    fetch_data.s(url) |
    process_data.s() |
    save_results.s()
)
result = workflow.apply_async()
```

### Groups
```python
from celery import group

# Parallel execution
job = group([
    add.s(2, 2),
    add.s(4, 4),
    add.s(8, 8),
])
result = job.apply_async()

# Wait for all results
results = result.get(timeout=10)  # [4, 8, 16]

# Group with callbacks
job = group([
    process_item.s(item) for item in items
]) | summarize_results.s()
```

### Chords
```python
from celery import chord

# Group with callback
job = chord([
    fetch_url.s(url) for url in urls
])(combine_results.s())

# Example: Process multiple files, then merge
workflow = chord([
    process_file.s(file) for file in files
])(merge_results.s())

result = workflow.apply_async()
```

### Map and Starmap
```python
from celery import group

# Map: Apply same task to list of args
results = add.map([(2, 2), (4, 4), (8, 8)])

# Starmap: Unpack arguments
results = add.starmap([(2, 2), (4, 4), (8, 8)])

# Equivalent to:
results = group([add.s(2, 2), add.s(4, 4), add.s(8, 8)])()
```

### Complex Workflows
```python
from celery import chain, group, chord

# Parallel processing with sequential steps
workflow = chain(
    # Step 1: Fetch data
    fetch_data.s(source),

    # Step 2: Process in parallel
    group([
        process_chunk.s(chunk_id) for chunk_id in range(10)
    ]),

    # Step 3: Aggregate results
    aggregate.s(),

    # Step 4: Save to database
    save_results.s()
)

# Nested chords
workflow = chord([
    chord([
        subtask.s(item) for item in chunk
    ])(process_chunk.s())
    for chunk in chunks
])(final_callback.s())

# Real-world example: Report generation
generate_report = chain(
    fetch_user_data.s(user_id),
    chord([
        calculate_stats.s(),
        fetch_transactions.s(),
        fetch_activity.s(),
    ])(combine_sections.s()),
    render_pdf.s(),
    send_email.s(user_email)
)
```

---

## Error Handling

### Automatic Retries
```python
@app.task(
    autoretry_for=(RequestException, IOError),  # Auto-retry these exceptions
    retry_kwargs={'max_retries': 5},             # Max 5 retries
    retry_backoff=True,                          # Exponential backoff
    retry_backoff_max=600,                       # Max 10 minutes backoff
    retry_jitter=True,                           # Add randomness to backoff
)
def fetch_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
```

### Manual Retries
```python
@app.task(bind=True, max_retries=3)
def process_data(self, data):
    try:
        result = external_api_call(data)
        return result
    except TemporaryError as exc:
        # Retry after 60 seconds
        raise self.retry(exc=exc, countdown=60)
    except PermanentError as exc:
        # Don't retry, log and fail
        logger.error(f"Permanent error: {exc}")
        raise
    except Exception as exc:
        # Exponential backoff
        raise self.retry(
            exc=exc,
            countdown=2 ** self.request.retries,
            max_retries=3
        )
```

### Error Callbacks
```python
@app.task
def on_error(request, exc, traceback):
    """Called when task fails"""
    logger.error(f"Task {request.id} failed: {exc}")
    send_alert(f"Task failure: {request.task}", str(exc))

@app.task
def risky_task(data):
    return process(data)

# Link error callback
risky_task.apply_async(
    args=(data,),
    link_error=on_error.s()
)
```

### Task Failure Handling
```python
from celery import Task

class CallbackTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Handle task failure"""
        logger.error(f"Task {task_id} failed with {exc}")
        # Send notification
        send_notification('Task Failed', str(exc))

    def on_success(self, retval, task_id, args, kwargs):
        """Handle task success"""
        logger.info(f"Task {task_id} succeeded: {retval}")

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """Handle task retry"""
        logger.warning(f"Task {task_id} retrying: {exc}")

@app.task(base=CallbackTask)
def monitored_task(x):
    if x < 0:
        raise ValueError("Negative value")
    return x * 2
```

### Exception Handling Patterns
```python
@app.task(bind=True)
def robust_task(self, data):
    # Categorize exceptions
    try:
        return process(data)

    except NetworkError as exc:
        # Transient error - retry
        raise self.retry(exc=exc, countdown=60, max_retries=5)

    except ValidationError as exc:
        # Permanent error - don't retry
        logger.error(f"Invalid data: {exc}")
        return {'status': 'failed', 'error': str(exc)}

    except DatabaseError as exc:
        # Critical error - retry with exponential backoff
        backoff = min(2 ** self.request.retries * 60, 3600)
        raise self.retry(exc=exc, countdown=backoff, max_retries=10)

    except Exception as exc:
        # Unknown error - retry limited times
        if self.request.retries < 3:
            raise self.retry(exc=exc, countdown=120)
        else:
            # Max retries exceeded - fail and alert
            logger.critical(f"Task failed after retries: {exc}")
            send_alert('Critical Task Failure', str(exc))
            raise
```

---

## Monitoring and Management

### Task Events
```python
# Enable events
app.conf.worker_send_task_events = True
app.conf.task_send_sent_event = True

# Event listeners
from celery import signals

@signals.task_prerun.connect
def task_prerun_handler(sender=None, task_id=None, task=None, args=None, kwargs=None, **extra):
    print(f"Task {task.name}[{task_id}] starting")

@signals.task_postrun.connect
def task_postrun_handler(sender=None, task_id=None, task=None, retval=None, **extra):
    print(f"Task {task.name}[{task_id}] completed: {retval}")

@signals.task_failure.connect
def task_failure_handler(sender=None, task_id=None, exception=None, traceback=None, **extra):
    print(f"Task {task_id} failed: {exception}")

@signals.task_retry.connect
def task_retry_handler(sender=None, task_id=None, reason=None, **extra):
    print(f"Task {task_id} retrying: {reason}")
```

### Flower Monitoring
```bash
# Install Flower
pip install flower

# Start Flower
celery -A myapp flower --port=5555

# Access dashboard
# http://localhost:5555
```

```python
# Flower configuration
flower_basic_auth = ['admin:password']
flower_persistent = True
flower_db = 'flower.db'
flower_max_tasks = 10000
```

### Inspecting Workers
```python
from celery_app import app

# Get active tasks
i = app.control.inspect()
print(i.active())

# Get scheduled tasks
print(i.scheduled())

# Get reserved tasks
print(i.reserved())

# Get worker stats
print(i.stats())

# Get registered tasks
print(i.registered())

# Revoke task
app.control.revoke(task_id, terminate=True)

# Shutdown worker
app.control.shutdown()

# Pool restart
app.control.pool_restart()

# Rate limit
app.control.rate_limit('myapp.tasks.slow_task', '10/m')
```

### Command Line Inspection
```bash
# List active tasks
celery -A myapp inspect active

# List scheduled tasks
celery -A myapp inspect scheduled

# Worker stats
celery -A myapp inspect stats

# Registered tasks
celery -A myapp inspect registered

# Revoke task
celery -A myapp control revoke <task_id>

# Shutdown workers
celery -A myapp control shutdown

# Purge all tasks
celery -A myapp purge
```

### Custom Metrics
```python
@app.task(bind=True)
def tracked_task(self, data):
    from prometheus_client import Counter, Histogram

    task_counter = Counter('celery_tasks_total', 'Total tasks')
    task_duration = Histogram('celery_task_duration_seconds', 'Task duration')

    with task_duration.time():
        result = process(data)
        task_counter.inc()
        return result
```

---

## Framework Integration

### Django Integration
```python
# myproject/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# myproject/__init__.py
from .celery import app as celery_app
__all__ = ('celery_app',)

# settings.py
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True

# Task in Django app
# myapp/tasks.py
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_email_task(subject, message, recipient):
    send_mail(subject, message, 'from@example.com', [recipient])
    return f"Email sent to {recipient}"

# Use in views
from myapp.tasks import send_email_task

def my_view(request):
    send_email_task.delay('Hello', 'Welcome!', 'user@example.com')
    return HttpResponse('Email queued')
```

### FastAPI Integration
```python
# celery_app.py
from celery import Celery

celery_app = Celery(
    'fastapi_app',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1'
)

@celery_app.task
def process_data(data: dict):
    # Long-running task
    import time
    time.sleep(10)
    return {"processed": data, "status": "complete"}

# main.py
from fastapi import FastAPI, BackgroundTasks
from celery_app import process_data

app = FastAPI()

@app.post("/process")
async def process_endpoint(data: dict):
    # Option 1: FastAPI BackgroundTasks (simple, in-process)
    # background_tasks.add_task(process_data, data)

    # Option 2: Celery (distributed, persistent)
    task = process_data.delay(data)
    return {"task_id": task.id, "status": "queued"}

@app.get("/status/{task_id}")
async def check_status(task_id: str):
    from celery.result import AsyncResult
    task = AsyncResult(task_id, app=celery_app)

    return {
        "task_id": task_id,
        "status": task.status,
        "result": task.result if task.ready() else None
    }
```

**When to Use Celery vs FastAPI BackgroundTasks**:
- **FastAPI BackgroundTasks**: Simple, fire-and-forget tasks (logging, cleanup)
- **Celery**: Distributed processing, retries, scheduling, task results

### Flask Integration
```python
# celery_app.py
from celery import Celery

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

# app.py
from flask import Flask
from celery_app import make_celery

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/1'

celery = make_celery(app)

@celery.task
def send_email(to, subject, body):
    with app.app_context():
        # Use Flask-Mail or similar
        mail.send(Message(subject, recipients=[to], body=body))

@app.route('/send')
def send_route():
    send_email.delay('user@example.com', 'Hello', 'Welcome!')
    return 'Email queued'
```

---

## Testing Strategies

### Eager Mode (Synchronous Execution)
```python
# conftest.py (pytest)
import pytest
from celery_app import app

@pytest.fixture(scope='session')
def celery_config():
    return {
        'broker_url': 'memory://',
        'result_backend': 'cache+memory://',
        'task_always_eager': True,          # Execute tasks synchronously
        'task_eager_propagates': True,      # Propagate exceptions
    }

# Test tasks
def test_add_task():
    result = add.delay(4, 6)
    assert result.get() == 10

def test_task_failure():
    with pytest.raises(ValueError):
        failing_task.delay()
```

### Testing with Real Broker
```python
# conftest.py
import pytest
from celery_app import app

@pytest.fixture(scope='session')
def celery_config():
    return {
        'broker_url': 'redis://localhost:6379/15',  # Test database
        'result_backend': 'redis://localhost:6379/15',
    }

@pytest.fixture
def celery_worker(celery_app):
    """Start worker for tests"""
    with celery_app.Worker() as worker:
        yield worker

def test_async_task(celery_worker):
    result = async_task.delay(data)
    assert result.get(timeout=10) == expected
```

### Mocking External Dependencies
```python
from unittest.mock import patch, MagicMock

@app.task
def fetch_and_process(url):
    response = requests.get(url)
    return process(response.json())

def test_fetch_and_process():
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {'data': 'test'}

        result = fetch_and_process.delay('http://example.com')
        assert result.get() == expected_result
        mock_get.assert_called_once_with('http://example.com')
```

### Testing Periodic Tasks
```python
from celery.schedules import crontab

def test_periodic_task_schedule():
    from celery_app import app

    schedule = app.conf.beat_schedule['daily-report']
    assert schedule['task'] == 'myapp.tasks.daily_report'
    assert schedule['schedule'] == crontab(hour=0, minute=0)

def test_periodic_task_execution():
    # Test task logic directly
    result = daily_report()
    assert result['status'] == 'complete'
```

### Integration Testing
```python
import pytest
from celery_app import app

@pytest.fixture(scope='module')
def celery_app():
    app.conf.update(
        broker_url='redis://localhost:6379/15',
        result_backend='redis://localhost:6379/15',
    )
    return app

@pytest.fixture(scope='module')
def celery_worker(celery_app):
    with celery_app.Worker() as worker:
        yield worker

def test_workflow(celery_worker):
    from celery import chain

    workflow = chain(
        fetch_data.s(url),
        process_data.s(),
        save_results.s()
    )

    result = workflow.apply_async()
    output = result.get(timeout=30)

    assert output['status'] == 'saved'
```

---

## Production Patterns

### Worker Configuration
```bash
# Production worker with autoscaling
celery -A myapp worker \
  --autoscale=10,3 \
  --max-tasks-per-child=1000 \
  --time-limit=300 \
  --soft-time-limit=240 \
  --loglevel=info \
  --logfile=/var/log/celery/worker.log \
  --pidfile=/var/run/celery/worker.pid

# Multiple specialized workers
celery multi start \
  worker1 -A myapp -Q high_priority -c 4 --max-tasks-per-child=100 \
  worker2 -A myapp -Q default -c 2 --max-tasks-per-child=1000 \
  worker3 -A myapp -Q low_priority -c 1 --autoscale=3,1

# Graceful shutdown
celery multi stop worker1 worker2 worker3
celery multi stopwait worker1 worker2 worker3  # Wait for tasks to finish
```

### Configuration Best Practices
```python
# production_config.py
import os

# Broker settings
broker_url = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
broker_connection_retry_on_startup = True
broker_pool_limit = 50

# Result backend
result_backend = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/1')
result_expires = 3600  # 1 hour

# Serialization
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'UTC'
enable_utc = True

# Performance
worker_prefetch_multiplier = 4  # Tasks to prefetch per worker
worker_max_tasks_per_child = 1000  # Restart worker after N tasks (prevent memory leaks)
task_acks_late = True  # Acknowledge after task completes
task_reject_on_worker_lost = True  # Requeue if worker dies

# Reliability
task_track_started = True  # Track when task starts
task_time_limit = 300  # 5 minutes hard limit
task_soft_time_limit = 240  # 4 minutes soft limit

# Logging
worker_log_format = '[%(asctime)s: %(levelname)s/%(processName)s] %(message)s'
worker_task_log_format = '[%(asctime)s: %(levelname)s/%(processName)s][%(task_name)s(%(task_id)s)] %(message)s'
```

### Systemd Service
```ini
# /etc/systemd/system/celery.service
[Unit]
Description=Celery Service
After=network.target redis.target

[Service]
Type=forking
User=celery
Group=celery
WorkingDirectory=/opt/myapp
Environment="PATH=/opt/myapp/venv/bin"
ExecStart=/opt/myapp/venv/bin/celery multi start worker1 \
    -A myapp \
    --pidfile=/var/run/celery/%n.pid \
    --logfile=/var/log/celery/%n%I.log \
    --loglevel=INFO
ExecStop=/opt/myapp/venv/bin/celery multi stopwait worker1 \
    --pidfile=/var/run/celery/%n.pid
ExecReload=/opt/myapp/venv/bin/celery multi restart worker1 \
    -A myapp \
    --pidfile=/var/run/celery/%n.pid \
    --logfile=/var/log/celery/%n%I.log \
    --loglevel=INFO
Restart=always

[Install]
WantedBy=multi-user.target

# /etc/systemd/system/celerybeat.service
[Unit]
Description=Celery Beat Service
After=network.target redis.target

[Service]
Type=simple
User=celery
Group=celery
WorkingDirectory=/opt/myapp
Environment="PATH=/opt/myapp/venv/bin"
ExecStart=/opt/myapp/venv/bin/celery -A myapp beat \
    --loglevel=INFO \
    --pidfile=/var/run/celery/beat.pid
Restart=always

[Install]
WantedBy=multi-user.target
```

### Sentry Integration
```python
# Install
pip install sentry-sdk

# Configuration
import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration

sentry_sdk.init(
    dsn="https://your-sentry-dsn",
    integrations=[CeleryIntegration()],
    traces_sample_rate=0.1,  # 10% of transactions
)

# Tasks are automatically tracked
@app.task
def my_task(x):
    # Exceptions automatically sent to Sentry
    return risky_operation(x)
```

### Rate Limiting
```python
# Global rate limiting
app.conf.task_default_rate_limit = '100/m'  # 100 tasks per minute

# Per-task rate limiting
@app.task(rate_limit='10/m')
def rate_limited_task(x):
    return expensive_operation(x)

# Dynamic rate limiting
app.control.rate_limit('myapp.tasks.slow_task', '5/m')

# Token bucket rate limiting
@app.task(rate_limit='10/s')
def api_call(endpoint):
    return requests.get(endpoint)
```

### Health Checks
```python
# health.py
from celery_app import app

def check_celery_health():
    """Health check endpoint"""
    try:
        # Ping workers
        i = app.control.inspect()
        stats = i.stats()

        if not stats:
            return {'status': 'unhealthy', 'reason': 'No workers available'}

        # Check broker connection
        result = app.control.ping(timeout=1.0)
        if not result:
            return {'status': 'unhealthy', 'reason': 'Workers not responding'}

        return {'status': 'healthy', 'workers': len(stats)}
    except Exception as e:
        return {'status': 'unhealthy', 'error': str(e)}

# FastAPI health endpoint
@app.get("/health/celery")
async def celery_health():
    return check_celery_health()
```

---

## Performance Optimization

### Task Optimization
```python
# Use ignore_result for fire-and-forget tasks
@app.task(ignore_result=True)
def send_notification(user_id, message):
    # Don't need result, save backend overhead
    notify(user_id, message)

# Compression for large payloads
@app.task(compression='gzip')
def process_large_data(data):
    return analyze(data)

# Serialization choice
@app.task(serializer='msgpack')  # Faster than JSON
def fast_task(data):
    return process(data)
```

### Worker Tuning
```python
# Worker concurrency
worker_concurrency = 4  # CPU-bound: num_cores
worker_concurrency = 20  # I/O-bound: higher value

# Prefetch multiplier (how many tasks to prefetch)
worker_prefetch_multiplier = 4  # Balance: 4x concurrency

# Task acknowledgment
task_acks_late = True  # Acknowledge after completion (reliability)
task_acks_late = False  # Acknowledge on receipt (performance)

# Memory management
worker_max_tasks_per_child = 1000  # Restart worker after N tasks
worker_max_memory_per_child = 200000  # Restart after 200MB
```

### Database Result Backend Optimization
```python
# Use Redis instead of database for results
result_backend = 'redis://localhost:6379/1'

# If using database, optimize
result_backend = 'db+postgresql://user:pass@localhost/celery'
database_engine_options = {
    'pool_size': 20,
    'pool_recycle': 3600,
}

# Reduce result expiry time
result_expires = 3600  # 1 hour instead of default 24 hours
```

### Task Chunking
```python
from celery import group

# Bad: One task per item (overhead)
for item in large_list:
    process_item.delay(item)

# Good: Chunk items
def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

@app.task
def process_batch(items):
    return [process_item(item) for item in items]

# Process in batches of 100
job = group(process_batch.s(chunk) for chunk in chunks(large_list, 100))
result = job.apply_async()
```

### Connection Pooling
```python
# Redis connection pool
broker_pool_limit = 50  # Max connections to broker
redis_max_connections = 50

# Database connection pool
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    'postgresql://user:pass@localhost/db',
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=0,
)
```

---

## Common Use Cases

### Email Sending
```python
@app.task(bind=True, max_retries=3)
def send_email_task(self, to, subject, body, attachments=None):
    try:
        msg = EmailMessage(subject, body, 'from@example.com', [to])
        if attachments:
            for filename, content, mimetype in attachments:
                msg.attach(filename, content, mimetype)
        msg.send()
        return {'status': 'sent', 'to': to}
    except SMTPException as exc:
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))

# Bulk email with rate limiting
@app.task(rate_limit='100/m')
def send_bulk_email(recipients, subject, template):
    for recipient in recipients:
        send_email_task.delay(recipient, subject, render_template(template, recipient))
```

### Report Generation
```python
@app.task(bind=True, time_limit=600)
def generate_report(self, report_type, user_id, start_date, end_date):
    # Update progress
    self.update_state(state='PROGRESS', meta={'current': 0, 'total': 100})

    # Fetch data
    data = fetch_report_data(report_type, start_date, end_date)
    self.update_state(state='PROGRESS', meta={'current': 30, 'total': 100})

    # Generate PDF
    pdf = render_pdf(data)
    self.update_state(state='PROGRESS', meta={'current': 70, 'total': 100})

    # Upload to S3
    url = upload_to_s3(pdf, f'reports/{user_id}/{report_type}.pdf')
    self.update_state(state='PROGRESS', meta={'current': 90, 'total': 100})

    # Send notification
    send_email_task.delay(
        get_user_email(user_id),
        'Report Ready',
        f'Your report is ready: {url}'
    )

    return {'status': 'complete', 'url': url}

# Check progress
from celery.result import AsyncResult

task = AsyncResult(task_id)
if task.state == 'PROGRESS':
    print(task.info)  # {'current': 30, 'total': 100}
```

### Data Processing Pipeline
```python
from celery import chain, group

@app.task
def fetch_data(source):
    return download(source)

@app.task
def clean_data(raw_data):
    return clean(raw_data)

@app.task
def transform_data(clean_data):
    return transform(clean_data)

@app.task
def load_data(transformed_data):
    save_to_database(transformed_data)
    return {'status': 'loaded', 'rows': len(transformed_data)}

# ETL pipeline
etl_pipeline = chain(
    fetch_data.s('https://api.example.com/data'),
    clean_data.s(),
    transform_data.s(),
    load_data.s()
)

result = etl_pipeline.apply_async()
```

### Webhook Processing
```python
@app.task(bind=True, autoretry_for=(RequestException,), max_retries=5)
def process_webhook(self, webhook_data):
    # Validate signature
    if not verify_signature(webhook_data):
        raise ValueError("Invalid signature")

    # Process event
    event_type = webhook_data['type']

    if event_type == 'payment.success':
        update_order_status(webhook_data['order_id'], 'paid')
        send_confirmation_email.delay(webhook_data['customer_email'])

    elif event_type == 'payment.failed':
        notify_admin.delay('Payment Failed', webhook_data)

    return {'status': 'processed', 'event': event_type}

# FastAPI webhook endpoint
@app.post("/webhooks/stripe")
async def stripe_webhook(request: Request):
    data = await request.json()
    process_webhook.delay(data)
    return {"status": "queued"}
```

### Image Processing
```python
from celery import group, chord

@app.task
def resize_image(image_path, size):
    from PIL import Image
    img = Image.open(image_path)
    img.thumbnail(size)
    output_path = f"{image_path}_{size[0]}x{size[1]}.jpg"
    img.save(output_path)
    return output_path

@app.task
def upload_to_cdn(image_paths):
    urls = []
    for path in image_paths:
        url = cdn_upload(path)
        urls.append(url)
    return urls

# Generate multiple sizes and upload
def process_uploaded_image(image_path):
    sizes = [(800, 600), (400, 300), (200, 150), (100, 100)]

    workflow = chord([
        resize_image.s(image_path, size) for size in sizes
    ])(upload_to_cdn.s())

    return workflow.apply_async()
```

---

## Alternatives Comparison

### Celery vs RQ (Redis Queue)
**RQ**: Simpler Redis-only task queue

**When to use RQ**:
- Simple use case (no routing, basic retries)
- Redis-only infrastructure
- Python 3 only
- Smaller scale (<1000 tasks/min)

**When to use Celery**:
- Complex workflows (chains, chords)
- Multiple broker options
- Advanced routing and priorities
- Large scale (>1000 tasks/min)
- Periodic tasks

```python
# RQ Example
from redis import Redis
from rq import Queue

redis_conn = Redis()
q = Queue(connection=redis_conn)

job = q.enqueue(my_function, arg1, arg2)
result = job.result
```

### Celery vs Huey
**Huey**: Lightweight task queue with minimal dependencies

**When to use Huey**:
- Small to medium projects
- Minimal configuration
- Redis or in-memory only
- Simple periodic tasks

**When to use Celery**:
- Enterprise-scale applications
- Complex task dependencies
- Multiple broker/backend options
- Advanced monitoring needs

```python
# Huey Example
from huey import RedisHuey

huey = RedisHuey('myapp')

@huey.task()
def add(a, b):
    return a + b

result = add(1, 2)
```

### Celery vs Dramatiq
**Dramatiq**: Modern alternative focusing on reliability

**When to use Dramatiq**:
- Reliability over features
- Simpler API
- Better type hints
- RabbitMQ or Redis

**When to use Celery**:
- Mature ecosystem
- More broker options
- Canvas workflows
- Larger community

```python
# Dramatiq Example
import dramatiq

@dramatiq.actor
def add(x, y):
    return x + y

add.send(1, 2)
```

### Celery vs Cloud Services
**AWS Lambda, Google Cloud Functions, Azure Functions**

**When to use Cloud Functions**:
- Serverless infrastructure
- Event-driven workflows
- Pay-per-execution model
- Auto-scaling

**When to use Celery**:
- Self-hosted infrastructure
- Complex task workflows
- Cost predictability
- Full control over execution

---

## Best Practices

### Task Design
1. **Idempotency**: Tasks should be safe to run multiple times
   ```python
   @app.task
   def process_order(order_id):
       order = Order.objects.get(id=order_id)
       if order.status == 'processed':
           return  # Already processed, skip

       order.process()
       order.status = 'processed'
       order.save()
   ```

2. **Small, Focused Tasks**: One responsibility per task
   ```python
   # Bad: Monolithic task
   @app.task
   def process_user(user_id):
       send_welcome_email(user_id)
       create_profile(user_id)
       setup_notifications(user_id)

   # Good: Separate tasks
   @app.task
   def send_welcome_email(user_id):
       ...

   @app.task
   def create_profile(user_id):
       ...

   workflow = group([
       send_welcome_email.s(user_id),
       create_profile.s(user_id),
       setup_notifications.s(user_id)
   ])
   ```

3. **Avoid Database Objects in Arguments**: Use IDs instead
   ```python
   # Bad
   @app.task
   def process_user(user):  # User object
       ...

   # Good
   @app.task
   def process_user(user_id):
       user = User.objects.get(id=user_id)
       ...
   ```

4. **Set Time Limits**: Prevent runaway tasks
   ```python
   @app.task(time_limit=300, soft_time_limit=240)
   def bounded_task():
       ...
   ```

### Error Handling
1. **Categorize Exceptions**: Different handling for different errors
2. **Use Exponential Backoff**: Avoid overwhelming failing services
3. **Set Max Retries**: Don't retry forever
4. **Log Failures**: Always log why tasks fail

### Performance
1. **Use `ignore_result=True`**: For tasks that don't need results
2. **Batch Operations**: Process multiple items per task
3. **Optimize Serialization**: Use msgpack for speed
4. **Connection Pooling**: Reuse database/broker connections
5. **Task Chunking**: Avoid creating millions of tiny tasks

### Monitoring
1. **Enable Events**: Track task lifecycle
2. **Use Flower**: Web-based monitoring
3. **Health Checks**: Monitor worker availability
4. **Sentry Integration**: Track errors

### Security
1. **Validate Input**: Always validate task arguments
2. **Secure Broker**: Use authentication and encryption
3. **Limit Task Execution Time**: Prevent resource exhaustion
4. **Rate Limiting**: Protect against task flooding

---

## Troubleshooting

### Tasks Not Executing
**Symptoms**: Tasks queued but not processing

**Diagnosis**:
```bash
# Check if workers are running
celery -A myapp inspect active

# Check worker stats
celery -A myapp inspect stats

# Check registered tasks
celery -A myapp inspect registered
```

**Solutions**:
- Start workers: `celery -A myapp worker`
- Check worker is consuming correct queues
- Verify task routing configuration
- Check broker connectivity

### Tasks Failing Silently
**Symptoms**: Tasks show SUCCESS but don't work

**Diagnosis**:
```python
# Enable task tracking
app.conf.task_track_started = True

# Check task result and traceback
result = task.delay()
if result.failed():
    print(result.traceback)
```

**Solutions**:
- Check logs: `celery -A myapp worker --loglevel=debug`
- Enable eager mode in tests to see exceptions
- Use `task_eager_propagates = True` in tests

### Memory Leaks
**Symptoms**: Worker memory grows over time

**Solutions**:
```python
# Restart workers after N tasks
worker_max_tasks_per_child = 1000

# Restart on memory limit
worker_max_memory_per_child = 200000  # 200MB
```

### Slow Task Execution
**Symptoms**: Tasks taking longer than expected

**Diagnosis**:
```python
# Add timing
import time

@app.task(bind=True)
def timed_task(self):
    start = time.time()
    result = slow_operation()
    duration = time.time() - start
    logger.info(f"Task {self.request.id} took {duration}s")
    return result
```

**Solutions**:
- Increase worker concurrency
- Optimize task code
- Use task chunking
- Add more workers

### Broker Connection Issues
**Symptoms**: Tasks not reaching workers

**Diagnosis**:
```bash
# Test broker connection
python -c "from celery_app import app; print(app.connection().connect())"
```

**Solutions**:
- Check broker is running: `redis-cli ping` or `rabbitmqctl status`
- Verify broker URL in configuration
- Check network connectivity
- Enable connection retry: `broker_connection_retry_on_startup = True`

### Task Results Not Persisting
**Symptoms**: `result.get()` returns None

**Solutions**:
- Verify result backend configured
- Check task doesn't have `ignore_result=True`
- Verify result hasn't expired (`result_expires`)
- Test backend connection

### Beat Not Scheduling Tasks
**Symptoms**: Periodic tasks not running

**Diagnosis**:
```bash
# Check beat is running
ps aux | grep celery | grep beat

# Check beat schedule
celery -A myapp inspect scheduled
```

**Solutions**:
- Ensure beat process is running
- Verify `beat_schedule` configuration
- Check beat log for errors
- Use database scheduler for dynamic schedules

### Worker Crashes
**Symptoms**: Workers die unexpectedly

**Solutions**:
- Check logs for errors
- Set `worker_max_tasks_per_child` to prevent memory leaks
- Add task time limits
- Use systemd for automatic restart
- Monitor with Flower

### Task Queue Buildup
**Symptoms**: Tasks accumulating in queue

**Solutions**:
- Add more workers
- Increase worker concurrency
- Optimize slow tasks
- Add task routing to distribute load
- Check for blocked workers

---

## Advanced Configuration

### Custom Task Classes
```python
from celery import Task

class DatabaseTask(Task):
    """Task that manages database connections"""
    _db = None

    @property
    def db(self):
        if self._db is None:
            self._db = create_db_connection()
        return self._db

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        """Close connection after task"""
        if self._db is not None:
            self._db.close()

@app.task(base=DatabaseTask)
def db_task(query):
    return db_task.db.execute(query)
```

### Custom Serializers
```python
from kombu.serialization import register

def my_encoder(obj):
    # Custom encoding logic
    return json.dumps(obj)

def my_decoder(data):
    # Custom decoding logic
    return json.loads(data)

register('myjson', my_encoder, my_decoder,
         content_type='application/x-myjson',
         content_encoding='utf-8')

app.conf.task_serializer = 'myjson'
```

### Task Inheritance
```python
class BaseTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        send_alert(f"Task {self.name} failed", str(exc))

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        logger.warning(f"Task {self.name} retrying")

@app.task(base=BaseTask)
def monitored_task():
    return perform_work()
```

---

**End of Celery Skill Documentation**

For more information:
- Official Documentation: https://docs.celeryq.dev/
- GitHub: https://github.com/celery/celery
- Community: https://groups.google.com/forum/#!forum/celery-users

## Related Skills

When using Celery, these skills enhance your workflow:
- **django**: Django + Celery integration for background tasks
- **fastapi-local-dev**: FastAPI + Celery patterns for async API operations
- **test-driven-development**: Testing async tasks and task chains
- **systematic-debugging**: Debugging distributed task failures and race conditions

[Full documentation available in these skills if deployed in your bundle]
