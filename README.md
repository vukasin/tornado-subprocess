tornado-subprocess
==================

A module which allows you to spawn subprocesses from a tornado web application in a non-blocking fashion.

Example:
--------
  
     def print_res( status, stdout, stderr, has_timed_out ) :
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
