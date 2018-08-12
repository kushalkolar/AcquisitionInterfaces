import abc
from threading import Thread
from queue import Queue
import tifffile
import cv2


class AbstractWriter(Thread):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, queue_in: Queue, queue_out: Queue, preview=True):
        Thread.__init__(self)
        self.queue_in = queue_in
        self.queue_out = queue_out
        self._preview = preview

    @abc.abstractmethod
    def run(self):
        pass

    @abc.abstractmethod
    def abort(self):
        pass


class TiffWriter(AbstractWriter):
    def __init__(self, queue_in: Queue, queue_out: Queue, filename: str, compression_level: int, preview=True):
        super().__init__(queue_in, queue_out, preview=preview)
        self.filename = filename
        self.compression_level = compression_level

        self.writer = tifffile.TiffWriter(filename, bigtiff=True, append=True)

        self._alive = True

    def run(self):
        while self._alive:

            if self.queue_in.empty():
                continue

            frame = self.queue_in.get()

            if type(frame) is str and frame == 'done':
                break

            self.writer.save(frame, compress=self.compression_level)

            cv2.imshow('Preview', frame)

            if self.queue_out is not None:
                self.queue_out.put(frame)
        self._stop()

    def _stop(self):
        self.writer.close()
        self._alive = False
        cv2.destroyWindow('Preview')

    def abort(self):
        self._stop()