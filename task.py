import traceback
from threading import Thread


class Task:
    def __init__(self, func, args):
        self.func = func
        self.args = args
        self.runner = None
        self.status = 'Stopped'

    def start_runner(self):
        if self.runner is not None:
            return
        self.status = 'Running'
        self.runner = Thread(target=self.thread, args=())
        self.runner.start()

    def thread(self):
        while True:
            if self.status == 'Wait stop':
                self.status = 'Stopped'
                break
            try:
                self.func(*self.args)
            except BaseException as e:
                traceback.print_tb(e.__traceback__)

    def stop_runner(self):
        if self.runner is None:
            return
        self.status = 'Wait stop'
        while self.status != 'Stopped':
            pass
        self.runner = None
