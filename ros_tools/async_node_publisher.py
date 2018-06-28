import os
import sys
import time
import threading
import uuid
import rospy
from collections import namedtuple

class AsyncNodePublisher(object):

    def __init__(self):
        self.Task = namedtuple('Task', 'uuid, rate, function, end_condition, completed')
        self.Callback = namedtuple('Callback', 'node_identifier, func')
        
        self._tasks = {}
        self._threads = {}
        
        self._task_lock = threading.Lock()
        self._thread_lock = threading.Lock()
        
        self._on_completed_funcs = []
        self._on_cancelled_funcs = []
                
        self._killall = False

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self._killall = True
        self._task_lock.acquire()
        for thread in self._threads.items():
            thread.join()
        for node_id, task in self._tasks.items():
            self._register_state_change(node_id, task, True)
        self._task_lock.release()
    
    def publish_async(self, node_identifier, rate, function, end_condition):
        request_uuid = uuid.uuid4()
        self._add_task(node_identifier, request_uuid, rate, function, end_condition)
        return request_uuid

    def register_on_completed_handler(self, callback):
        self._on_completed_funcs.append(callback)

    def register_on_cancelled_handler(self, callback):
        self._on_cancelled_funcs.append(callback)

    def _service_requests(self, rate):
        control_rate = rospy.Rate(rate)
        while (not rospy.is_shutdown() and not self._killall):
            self._execute_outstanding_tasks(rate)
            control_rate.sleep()
    
    def _execute_outstanding_tasks(self, rate):
        self._task_lock.acquire()
        for node_id, task in self._tasks.items():
            if(task.rate is rate and not task.completed):
                if(task.end_condition):
                    task = task._replace(completed = True)
                    self._register_state_change(node_id, task, False)
                else:
                    task.function
        self._task_lock.release()


    def _add_task(self, node_identifier, request_uuid, rate, function, end_condition):
        self._task_lock.acquire()
        self._tasks[node_identifier] = self.Task(uuid, rate, function, end_condition, False)
        self._task_lock.release()

        self._thread_lock.acquire()
        if not rate in self._threads:
            thread = threading.Thread(target=self._service_requests, args=(rate,))
            thread.daemon = True
            thread.start()
            self._threads[rate] = thread
        self._thread_lock.release()


    def _register_state_change(self, node_id, task, cancelled):
        if cancelled == True:
            for callback in self._on_cancelled_funcs:
                if(callback.node_identifier == node_id):
                    callback.func(task)
        else:
            for callback in self._on_completed_funcs:
                if(callback.node_identifier == node_id):
                    callback.func(task)
    
