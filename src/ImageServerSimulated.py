"""
Simulated backend for testing.
"""
import platform
import time
import logging
from io import BytesIO
from multiprocessing import Process, shared_memory, Condition, Lock
from PIL import Image, ImageDraw, ImageFont
import psutil
from pymitter import EventEmitter
from src.imageserverabstract import ImageServerAbstract, compile_buffer, decompile_buffer
from src.configsettings import settings

logger = logging.getLogger(__name__)


class ImageServerSimulated(ImageServerAbstract):
    """simulated backend to test photobooth"""

    def __init__(self, ee: EventEmitter, enableStream):
        super().__init__(ee, enableStream)

        # public props (defined in abstract class also)
        self.exif_make = "Photobooth FrameServer Simulate"
        self.exif_model = "Custom"
        self.metadata = {}

        # private props
        self._img_buffer_shm = shared_memory.SharedMemory(
            create=True,
            size=settings._shared_memory_buffer_size
        )
        self._condition_img_buffer_ready = Condition()
        self._img_buffer_lock = Lock()

        self._p = Process(
            target=img_aquisition,
            name="ImageServerSimulatedAquisitionProcess",
            args=(
                self._img_buffer_shm.name,
                self._condition_img_buffer_ready,
                self._img_buffer_lock
            ),
            daemon=True
        )

    def start(self):
        """To start the FrameServer"""

        self._p.start()
        logger.debug(f"{self.__module__} started")

    def stop(self):
        """To stop the FrameServer"""
        self._img_buffer_shm.close()
        self._img_buffer_shm.unlink()
        self._p.terminate()
        self._p.join(1)
        self._p.close()

        logger.debug(f"{self.__module__} stopped")

    def wait_for_hq_image(self):
        """for other threads to receive a hq JPEG image"""
        self._evtbus.emit("frameserver/onCapture")

        # get img off the producing queue
        with self._condition_img_buffer_ready:
            if not self._condition_img_buffer_ready.wait(2):
                raise IOError("timeout receiving frames")

            with self._img_buffer_lock:
                img = decompile_buffer(
                    self._img_buffer_shm)

        # virtual delay for camera to create picture
        time.sleep(0.1)

        self._evtbus.emit("frameserver/onCaptureFinished")

        # return to previewmode
        self._on_preview_mode()

        return img

    def gen_stream(self):
        last_time = time.time_ns()
        while True:
            now_time = time.time_ns()
            if (now_time-last_time)/1000**3 >= (1/settings.common.LIVEPREVIEW_FRAMERATE):
                last_time = now_time

                buffer = self._wait_for_lores_image()

                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer + b'\r\n\r\n')

    def trigger_hq_capture(self):
        self._on_capture_mode()

    #
    # INTERNAL FUNCTIONS
    #

    def _wait_for_lores_image(self):
        """for other threads to receive a lores JPEG image"""

        with self._condition_img_buffer_ready:
            if not self._condition_img_buffer_ready.wait(2):
                raise IOError("timeout receiving frames")

        with self._img_buffer_lock:

            img = decompile_buffer(
                self._img_buffer_shm)

        return img

    def _wait_for_lores_frame(self):
        """autofocus not supported by this backend"""
        raise NotImplementedError()

    def _on_capture_mode(self):
        logger.debug(
            "change to capture mode - means doing nothing in simulate")

    def _on_preview_mode(self):
        logger.debug(
            "change to preview mode - means doing nothing in simulate")

    #
    # INTERNAL IMAGE GENERATOR
    #


def img_aquisition(shm_buffer_name,
                   _condition_img_buffer_ready: Condition,
                   _img_buffer_lock: Lock):
    """ function started in separate process to deliver images """
    target_fps = 15
    last_time = time.time_ns()
    shm = shared_memory.SharedMemory(shm_buffer_name)

    while True:

        now_time = time.time_ns()
        if (now_time-last_time)/1000**3 <= (1/target_fps):
            # limit max framerate to every ~2ms
            time.sleep(2/1000.)
            continue

        fps = round(1/(now_time-last_time)*1000**3, 1)
        last_time = now_time

        # create PIL image
        img = Image.new(
            mode="RGB",
            size=(640,
                  480),
            color="green")

        # add text
        img_draw = ImageDraw.Draw(img)
        font_large = ImageFont.truetype(
            font="./vendor/fonts/Roboto/Roboto-Bold.ttf",
            size=30)
        font_small = ImageFont.truetype(
            font="./vendor/fonts/Roboto/Roboto-Bold.ttf",
            size=15)
        img_draw.text((100, 100),
                      "simulated image backend",
                      fill=(200, 200, 200),
                      font=font_large)
        img_draw.text((100, 140),
                      f"img time: {now_time}",
                      fill=(200, 200, 200),
                      font=font_large)
        img_draw.text((100, 180),
                      f"framerate: {fps}",
                      fill=(200, 200, 200),
                      font=font_large)
        img_draw.text((100, 220), (
            f"cpu: 1/5/15min "
            f"{[round(x / psutil.cpu_count() * 100,1) for x in psutil.getloadavg()]}%"
        ),
            fill=(200, 200, 200),
            font=font_large)
        img_draw.text((100, 260),
                      "you see this, so installation was successful :)",
                      fill=(200, 200, 200),
                      font=font_small)
        img_draw.text((100, 280),
                      f"goto http://{platform.node()}:{settings.common.webserver_port} to setup",
                      fill=(200, 200, 200),
                      font=font_small)
        img_draw.text((100, 300),
                      "to use a camera instead this simulated backend",
                      fill=(200, 200, 200),
                      font=font_small)

        # create jpeg
        jpeg_buffer = BytesIO()
        img.save(jpeg_buffer, format="jpeg", quality=90)

        # put jpeg on queue until full. If full this function blocks until queue empty
        with _img_buffer_lock:
            compile_buffer(shm, jpeg_buffer.getvalue())

        with _condition_img_buffer_ready:
            # wait to be notified
            _condition_img_buffer_ready.notify_all()
