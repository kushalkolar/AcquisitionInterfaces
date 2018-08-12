from multiprocessing import Process, Queue
# from queue import Queue
from cv2 import imshow


class Preview(Process):
    def __init__(self, queue: Queue):
        super(Preview, self).__init__()
        self.queue = queue

        self.alive = True

    def run(self):
        while self.alive:
            frame = self.queue.get()
            if not frame:
                break
            imshow('Preview', self.queue.get())

    def stop(self):
        self.alive = False
