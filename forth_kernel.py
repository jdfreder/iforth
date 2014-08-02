from IPython.kernel.zmq.kernelbase import Kernel

import signal
from subprocess import check_output, PIPE, Popen
from threading  import Thread
import re
import os
import sys
import time

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x

__version__ = '0.1'

class ForthKernel(Kernel):
    implementation = 'forth_kernel'
    implementation_version = __version__
    language = 'forth'

    @property
    def language_version(self):
        return self.banner.split(' ')[-1]

    _banner = None
    @property
    def banner(self):
        if self._banner is None:
            self._banner = check_output(['gforth', '--version']).decode('utf-8')
        return self._banner
    
    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        # TODO: Launch gforth
        ON_POSIX = 'posix' in sys.builtin_module_names

        def enqueue_output(out, queue):
            for line in iter(out.readline, b''):
                queue.put(line)
            out.close()

        self._gforth = Popen('gforth', stdin=PIPE, stdout=PIPE, bufsize=1, close_fds=ON_POSIX)

        self._gforth_que = Queue()
        t = Thread(target=enqueue_output, args=(self._gforth.stdout, self._gforth_que))
        t.daemon = True # thread dies with the program
        t.start()


    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        # Make sure we have code.
        code = code.strip()
        if not code:
            return {'status': 'ok', 'execution_count': self.execution_count,
                    'payload': [], 'user_expressions': {}}

        # Try running code...
        while not self._gforth_que.empty():
            line = self._gforth_que.get_nowait()
        self._gforth.stdin.write(code + '\n')
        # read line without blocking
        output = ''
        line = '.'
        timeout = 3.
        while len(line) > 0 or timeout > 0.:
            try:  
                line = self._gforth_que.get_nowait() # or q.get(timeout=.1)
            except Empty:
                line = ''
                if timeout > 0.:
                    time.sleep(0.01)
                    timeout -= 0.01
            else: # got line
                output += line + '\n'
                timeout = 0.

        # Return results.
        if not silent:
            stream_content = {'name': 'stdout', 'data': output}
            self.send_response(self.iopub_socket, 'stream', stream_content)
        
        # Barf or return ok.
        if False:
            return {'status': 'error', 'execution_count': self.execution_count,
                    'ename': '', 'evalue': str(exitcode), 'traceback': []}
        else:
            return {'status': 'ok', 'execution_count': self.execution_count,
                    'payload': [], 'user_expressions': {}}

if __name__ == '__main__':
    from IPython.kernel.zmq.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=ForthKernel)