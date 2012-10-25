"""
Copyright (c) 2012, Vukasin Toroman <vukasin@toroman.name>
"""

import subprocess
import tornado.ioloop
import time
import fcntl
import os

class Subprocess:
    """Thisclass is used to spawn subprocesses from a tornado.ioloop. The output of process is stored in memory (so don't use it to process large amounts of data)
        

        Example:
            def print_res( status, stdout, stderr ) :
                if status == 0:
                    print "OK:"
                    print stdout
                else:
                    print "ERROR:"
                    print stderr

            t = Subprocess( print_res, timeout=30, args=[ "cat", "/etc/passwd" ] )
            t.start()

            #start tornado 
            t.ioloop.start()            
"""
    def __init__ ( self, callback, timeout=-1, **popen_args ):
        """Create new instance

        Arguments:
            callback: method to be called after completion. This method should take 3 arguments: statuscode(int), stdout(str), stderr(str)
            timeout: wall time allocated for the process to complete. After this expires Task.cancel is called. A negative timeout value means no limit is set
            
        The task is not started until start is called. The process will then be spawned using subprocess.Popen(**popen_args). The stdout and stderr are always set to subprocess.PIPE.
        """
        self.stdout = []
        self.stderr = []
        popen_args["stdout"] = subprocess.PIPE
        popen_args["stderr"] = subprocess.PIPE
        self.callback = callback
        self.ioloop = None
        self.expiration = None
        self.pipe = None
        self.timeout = timeout
        self.streams = []
        self.args = popen_args

    def start(self):
        """Spawn the task.

        Throws RuntimeError if the task was already started."""
        if not self.pipe is None:
            raise RuntimeError("Cannot start task twice")

        self.ioloop = tornado.ioloop.IOLoop.instance()
        if self.timeout > 0:
            self.expiration = self.ioloop.add_timeout( time.time() + self.timeout, self.cancel )
        self.pipe = subprocess.Popen(**self.args)
        self.streams = [ (self.pipe.stdout.fileno(), []), 
                         (self.pipe.stderr.fileno(), []) ]
        for fd, d in self.streams:
            flags = fcntl.fcntl(fd, fcntl.F_GETFL)| os.O_NDELAY
            fcntl.fcntl( fd, fcntl.F_SETFL, flags)
            self.ioloop.add_handler( fd,
                                     self.stat,
                                     self.ioloop.READ|self.ioloop.ERROR)

    def cancel (self ) :
        """Cancel task execution

        Sends SIGKILL to the child process and triggers the callback."""
        self.pipe.kill()

    def stat( self, *args ):
        '''Check process completion and consume pending I/O data'''
        self.pipe.poll()
        if not self.pipe.returncode is None:
            '''cleanup handlers and timeouts'''
            if not self.expiration is None:
                self.ioloop.remove_timeout(self.expiration)
            for fd, dest in  self.streams:
                self.ioloop.remove_handler(fd)
            '''schedulle callback (first try to read all pending data)'''
            self.ioloop.add_callback(self.__do_callback)
        for fd, dest in  self.streams:
            while True:
		try:
			data = os.read(fd, 4096)
			if len(data) == 0:
			    break
			dest.extend([data])
		except:
			break	

    def __do_callback(self):
        if not self.callback is None:
            cb = self.callback
            '''prevent calling callback twice'''
            self.callback = None
            args  = [ self.pipe.returncode ] + [ "".join(s) for fd,s in self.streams ]
            cb(*args)
