from ipykernel.kernelbase import Kernel

from typing import Any, Dict
from subprocess import check_output, PIPE, Popen
from threading import Thread
from functools import cached_property
import re
import os
import sys
import time

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x

__version__ = '0.2'
__path__ = os.environ.get('GFORTHPATH')

class ForthKernel(Kernel):
    implementation = 'forth_kernel'
    implementation_version = __version__
    language = 'forth'
    first_command = True

    @property
    def language_version(self) -> str:
        return self.banner.split(' ')[-1]

    @cached_property
    def banner(self) -> str:
        return check_output(['gforth', '--version']).decode('utf-8')

    language_info = {
        'name': 'forth_kernel',
        'version': '0.2',
        'mimetype': 'text',
        'file_extension': '.4th'
	}

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        ON_POSIX = 'posix' in sys.builtin_module_names

        def enqueue_output(out, queue):
            for line in iter(out.readline, b''):
                queue.put(line)
            out.close()
        
        self._gforth = Popen('gforth', stdin=PIPE, stdout=PIPE, bufsize=2, close_fds=ON_POSIX)
        self._gforth_queue = Queue()

        t = Thread(target=enqueue_output, args=(self._gforth.stdout, self._gforth_queue))
        t.daemon = True
        t.start()


    def answer(self, output):
        stream_content = {'name': 'stdout', 'text': output}
        self.send_response(self.iopub_socket, 'stream', stream_content)

    def get_queue(self, queue):
        output = ''
        line = '.'
        timeout = 3.
        while len(line) or timeout > 0.:
            try:
                line = queue.get_nowait()
            except Empty:
                line = ''
                if timeout > 0.:
                    time.sleep(0.01)
                    timeout -= 0.01
            else:
                try:
                    output += line.decode()
                except UnicodeDecodeError:
                    output += line.decode('latin-1')
                timeout = 0.
        return output + '\n'


    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False) -> Dict[str, Any]:

        if self._gforth_queue.qsize():
            output = self.get_queue(self._gforth_queue)
        code = code.encode('utf-8') + '\n'.encode('utf-8')
        self._gforth.stdin.write(code)
        output = self.get_queue(self._gforth_queue)

        # Return results.
        if not silent:
            self.answer(output or 'None')

        return {'status': 'ok', 'execution_count': self.execution_count,
                'payload': [], 'user_expressions': {}}
    
if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    import shutil 

    assert shutil.which('gforth') is not None, 'Program gforth not found. Please install it and ensure it is on your Environment PATH.'
    IPKernelApp.launch_instance(kernel_class=ForthKernel)
