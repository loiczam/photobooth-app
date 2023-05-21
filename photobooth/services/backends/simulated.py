"""
Simulated backend for testing.
"""
import logging
import time
from datetime import datetime
from io import BytesIO
from multiprocessing import Condition, Event, Lock, Process, shared_memory

from PIL import Image, ImageDraw, ImageFont
from pymitter import EventEmitter

from ...appconfig import AppConfig
from ...utils.exceptions import ShutdownInProcessError
from .abstractbackend import (
    AbstractBackend,
    BackendStats,
    compile_buffer,
    decompile_buffer,
)

SHARED_MEMORY_BUFFER_BYTES = 1 * 1024**2

logger = logging.getLogger(__name__)


class SimulatedBackend(AbstractBackend):
    """simulated backend to test photobooth"""

    def __init__(self, evtbus: EventEmitter, config: AppConfig):
        super().__init__(evtbus, config)

        # public props (defined in abstract class also)
        self.metadata = {}

        # private props
        self._img_buffer_shm: shared_memory.SharedMemory
        self._condition_img_buffer_ready = Condition()
        self._img_buffer_lock = Lock()
        self._event_proc_shutdown: Event = Event()

        self._p: Process

    def start(self):
        """To start the image backend"""
        # ensure shutdown event is cleared (needed for restart during testing)
        self._event_proc_shutdown.clear()

        self._img_buffer_shm = shared_memory.SharedMemory(
            create=True,
            size=SHARED_MEMORY_BUFFER_BYTES,
        )

        self._p = Process(
            target=img_aquisition,
            name="SimulatedAquisitionProcess",
            args=(
                self._img_buffer_shm.name,
                self._condition_img_buffer_ready,
                self._img_buffer_lock,
                self._event_proc_shutdown,
            ),
            daemon=True,
        )
        # start process
        self._p.start()

        # block until startup completed, this ensures tests work well and backend for sure delivers images if requested
        remaining_retries = 10
        while True:
            with self._condition_img_buffer_ready:
                if self._condition_img_buffer_ready.wait(timeout=0.5):
                    break

                if remaining_retries < 0:
                    raise RuntimeError("failed to start up backend")

                remaining_retries -= 1
                logger.info("waiting for backend to start up...")

        logger.debug(f"{self.__module__} started")

    def stop(self):
        """To stop the image backend"""
        # signal process to shutdown properly
        self._event_proc_shutdown.set()

        # wait until shutdown finished
        self._p.join(timeout=1)
        self._p.close()

        self._img_buffer_shm.close()
        self._img_buffer_shm.unlink()

        logger.debug(f"{self.__module__} stopped")

    def wait_for_hq_image(self):
        """for other threads to receive a hq JPEG image"""
        self._evtbus.emit("frameserver/onCapture")

        # get img off the producing queue
        with self._condition_img_buffer_ready:
            if not self._condition_img_buffer_ready.wait(timeout=4):
                raise TimeoutError("timeout receiving frames")

            with self._img_buffer_lock:
                img = decompile_buffer(self._img_buffer_shm)

        # virtual delay for camera to create picture
        time.sleep(0.1)

        self._evtbus.emit("frameserver/onCaptureFinished")

        # return to previewmode
        self._on_preview_mode()

        return img

    def stats(self) -> BackendStats:
        return BackendStats(
            backend_name=__name__,
        )

    #
    # INTERNAL FUNCTIONS
    #

    def _wait_for_lores_image(self):
        """for other threads to receive a lores JPEG image"""
        if self._event_proc_shutdown.is_set():
            raise ShutdownInProcessError("shutdown already in progress, abort early")

        with self._condition_img_buffer_ready:
            if not self._condition_img_buffer_ready.wait(timeout=4):
                raise TimeoutError("timeout receiving frames")

        with self._img_buffer_lock:
            img = decompile_buffer(self._img_buffer_shm)

        return img

    def _wait_for_lores_frame(self):
        """autofocus not supported by this backend"""
        raise NotImplementedError()

    def _on_capture_mode(self):
        logger.debug("change to capture mode - means doing nothing in simulate")

    def _on_preview_mode(self):
        logger.debug("change to preview mode - means doing nothing in simulate")

    #
    # INTERNAL IMAGE GENERATOR
    #


def img_aquisition(
    shm_buffer_name,
    _condition_img_buffer_ready: Condition,
    _img_buffer_lock: Lock,
    _event_proc_shutdown: Event,
):
    """function started in separate process to deliver images"""
    target_fps = 15
    last_time = time.time_ns()
    shm = shared_memory.SharedMemory(shm_buffer_name)

    img_original = Image.open("./photobooth/assets/simulated_background.jpg")
    text_fill = "#888"

    while not _event_proc_shutdown.is_set():
        now_time = time.time_ns()
        if (now_time - last_time) / 1000**3 <= (1 / target_fps):
            # limit max framerate to every ~2ms
            time.sleep(2 / 1000.0)
            continue

        fps = round(1 / (now_time - last_time) * 1000**3, 1)
        last_time = now_time

        # create PIL image
        img = img_original.copy()

        # add text
        img_draw = ImageDraw.Draw(img)
        font_large = ImageFont.truetype(
            font="./photobooth/vendor/fonts/Roboto/Roboto-Bold.ttf", size=22
        )
        font_small = ImageFont.truetype(
            font="./photobooth/vendor/fonts/Roboto/Roboto-Bold.ttf", size=15
        )
        img_draw.text(
            (25, 100), "simulated image source", fill=text_fill, font=font_large
        )

        img_draw.text(
            (25, 130),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            fill=text_fill,
            font=font_large,
        )
        img_draw.text((25, 160), f"framerate: {fps}", fill=text_fill, font=font_small)
        img_draw.text(
            (25, 340),
            "you see this, so installation was successful :)",
            fill=text_fill,
            font=font_small,
        )

        # create jpeg
        jpeg_buffer = BytesIO()
        img.save(jpeg_buffer, format="jpeg", quality=90)

        # put jpeg on queue until full. If full this function blocks until queue empty
        with _img_buffer_lock:
            compile_buffer(shm, jpeg_buffer.getvalue())

        with _condition_img_buffer_ready:
            # wait to be notified
            _condition_img_buffer_ready.notify_all()
