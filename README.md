tornado-subprocess
==================

A module which allows you to spawn subprocesses from a tornado web application in a non-blocking fashion.Help on module tornado_subprocess:

NAME
    tornado_subprocess

FILE
    /Users/vukasin/tornado-subprocess/tornado_subprocess.py

DESCRIPTION
    Copyright (c) 2012, Vukasin Toroman <vukasin@toroman.name>
    All rights reserved.

CLASSES
    Subprocess
    
    class Subprocess
     |  Thisclass is used to spawn subprocesses from a tornado.ioloop. The output of process is stored in memory (so don't use it to process large amounts of data)
     |  
     |  
     |  Example:
     |      import task
     |  
     |      def print_res( status, stdout, stderr ) :
     |          if status == 0:
     |              print "OK:"
     |              print stdout
     |          else:
     |              print "ERROR:"
     |              print stderr
     |  
     |      t = Subprocess( print_res, timeout=30, args=[ "cat", "/etc/passwd" ] )
     |      t.start()
     |  
     |      #start tornado 
     |      t.ioloop.start()
     |  
     |  Methods defined here:
     |  
     |  __init__(self, callback, timeout=-1, **popen_args)
     |      Create new instance
     |      
     |      Arguments:
     |          callback: method to be called after completion. This method should take 3 arguments: statuscode(int), stdout(str), stderr(str)
     |          timeout: wall time allocated for the process to complete. After this expires Task.cancel is called. A negative timeout value means no limit is set
     |          
     |      The task is not started until start is called. The process will then be spawned using subprocess.Popen(**popen_args). The stdout and stderr are always set to subprocess.PIPE.
     |  
     |  cancel(self)
     |      Cancel task execution
     |      
     |      Sends SIGKILL to the child process and triggers the callback.
     |  
     |  start(self)
     |      Spawn the task.
     |      
     |      Throws RuntimeError if the task was already started.
     |  
     |  stat(self, *args)
     |      Check process completion and consume pending I/O data


