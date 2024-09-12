#Question 1: By default, are Django signals executed synchronously or asynchronously?
"""Answer: By default, Django signals are executed synchronously. 
This means that when a signal istriggered, the code that initiated
the signal must wait for the signal handler to complete before continuing.

"""

import time
import threading
from django.db.models.signals import task_save
from django.dispatch import receiver
from .models import Task

@receiver(task_save, sender=Task)
def notify_user_task_created(sender, instance, created, **kwargs):
    if created:
        print("Task creation signal started. Simulating delay to show synchronous behavior...")
        time.sleep(2)  # Simulating a 2-second delay

        print(f"Task '{instance.title}' created by {instance.author.username}. Signal processing completed.")



#Question 2: Do Django signals run in the same thread as the caller?
#Answer: Yes, Django signals run in the same thread as the caller by default.


import threading
from django.db.models.signals import task_save
from django.dispatch import receiver
from .models import Task

@receiver(task_save, sender=Task)
def notify_user_task_created(sender, instance, created, **kwargs):
    if created:
        # Check the current thread to prove signal runs in the same thread
        print(f"Signal running in thread: {threading.current_thread().name}")
        print(f"Task '{instance.title}' created by {instance.author.username}. Signal processing completed.")
        


#Question 3: By default, do Django signals run in the same database transaction as the caller?
"""Answer: Yes, by default, Django signals run in the same database transaction as the caller. 
If a signal handler throws an exception, it will cause the entire transaction,
including the original action (like saving a model), to be rolled back.
"""

#Question 3: By default, do Django signals run in the same database transaction as the caller?
'''Answer: Yes, by default, Django signals run in the same database transaction as the caller.
If a signal handler throws an exception, it will cause the entire transaction, including the 
original action (like saving a model), to be rolled back.'''   

from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task, UserTaskStatistics

@receiver(post_save, sender=Task)
def update_user_task_statistics(sender, instance, created, **kwargs):
    try:
        with transaction.atomic():
            user_stats, _ = UserTaskStatistics.objects.get_or_create(user=instance.author)

            if created:
                print(f"Updating task count for {instance.author.username}...")
                user_stats.task_count += 1
                user_stats.save()
                print(f"Task count updated to {user_stats.task_count} for {instance.author.username}.")

            if instance.is_completed and instance.completed_at:
                print(f"Updating completed task count for {instance.author.username}...")
                user_stats.completed_task_count += 1
                user_stats.save()
                print(f"Completed task count updated to {user_stats.completed_task_count} for {instance.author.username}.")
                
    except Exception as e:
        print(f"An error occurred: {e}. Rolling back transaction.")

#models 
from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

class UserTaskStatistics(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    task_count = models.IntegerField(default=0)
    completed_task_count = models.IntegerField(default=0)


  