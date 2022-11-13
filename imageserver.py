#!/usr/bin/python3

# ImageServer used to stream photos from raspberry pi camera for liveview and high quality capture while maintaining the stream
#
# Set up script as a service to run always in the background:
# https://medium.com/codex/setup-a-python-script-as-a-service-through-systemctl-systemd-f0cc55a42267


# TODO / Improvements
# 1) idea: cv2 face detection to autofocus on faces (might be to high load on RP)
# 2) add a way to change camera controls (sport mode, ...) to adapt for different lighting
# 3) improve autofocus algorithm
# 4) check tuning file: https://github.com/raspberrypi/picamera2/blob/main/examples/tuning_file.py

from datetime import datetime
import piexif
from PIL import Image
import traceback
from EventNotifier import Notifier
import json
import sys
import time
import cv2
from urllib.parse import parse_qs
import logging
from picamera2 import Picamera2
from lib.FrameServer import FrameServer
from lib.Autofocus import FocusState
# import for Arducam 16mp sony imx519
from lib.Focuser import Focuser
# from lib.FocuserImxArdu64 import Focuser    # import for Arducam 64mp
from lib.RepeatedTimer import RepeatedTimer
from lib.LocationService import LocationService
from http import server
import socketserver
import os
from lib.InfoLed import InfoLed
from config import CONFIG


# change to files path
os.chdir(sys.path[0])


# setup config object
config_instance = CONFIG()
config_instance.load()

# logger
logger = logging.getLogger(__name__)
logger.setLevel(config_instance.LOGGING_LEVEL)
fh = logging.StreamHandler()
fh_formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(lineno)d:%(filename)s(%(process)d) - %(message)s')
fh.setFormatter(fh_formatter)
logger.addHandler(fh)


def log_exceptions(type, value, tb):
    logger.exception(
        f"Uncaught exception: {str(value)} {(traceback.format_tb(tb))}")


# Install exception handler
sys.excepthook = log_exceptions

if config_instance.DEBUG_LOGFILE:
    fh2 = logging.FileHandler("/tmp/frameserver.log")
    fh2.setFormatter(fh_formatter)
    logger.addHandler(fh2)

notifier = Notifier(
    ["onTakePicture", "onTakePictureFinished", "onCountdownTakePicture", "onRefocus"], logger)


class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        # TODO serve directory: https://stackoverflow.com/questions/55052811/serve-directory-in-python-3
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            with open(f"web{self.path}", 'rb') as f:
                data = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.send_header('Content-Length', len(data))
                self.end_headers()
                self.wfile.write(data)
        elif self.path == '/stats/focuser':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

            self.wfile.write(json.dumps(
                focusState._lastRunResult).encode('utf8'))
        elif self.path == '/stats/locationservice':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

            self.wfile.write(json.dumps(
                locationService._geolocation_response).encode('utf8'))
        elif self.path == '/cmd/debug/on':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            logger.info(
                "enable debug")

            config_instance.DEBUG = True
            self.wfile.write(
                b'enable debug\r\n')
        elif self.path == '/cmd/debug/off':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            logger.info(
                "disable debug")

            config_instance.DEBUG = False
            self.wfile.write(
                b'disable debug\r\n')

        elif self.path == '/cmd/config/reset':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            logger.info(
                "reset config")
            config_instance.reset_default_values()
            self.wfile.write(
                b'reset config\r\n')
        elif self.path == '/cmd/config/save':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            logger.info(
                "save config")
            config_instance.save()
            self.wfile.write(
                b'save config\r\n')
        elif self.path == '/cmd/config/load':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            logger.info(
                "load config")
            config_instance.load()
            self.wfile.write(
                b'load config\r\n')
        elif self.path == '/cmd/debugoverlay/on':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            logger.info(
                "enable debugoverlay")
            config_instance.DEBUG_OVERLAY = True
            self.wfile.write(
                b'disable debugoverlay\r\n')
        elif self.path == '/cmd/debugoverlay/off':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            logger.info(
                "disable debugoverlay")
            config_instance.DEBUG_OVERLAY = False
            self.wfile.write(
                b'disable debugoverlay\r\n')
        elif self.path == '/cmd/exposuremode/normal':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            logger.info(
                "/cmd/exposuremode/normal")
            # enable overlay in frameserver
            config_instance.CAPTURE_EXPOSURE_MODE = "normal"
            frameServer.setAeExposureMode(
                config_instance.CAPTURE_EXPOSURE_MODE)
            self.wfile.write(
                b'/cmd/exposuremode/normal\r\n')
        elif self.path == '/cmd/exposuremode/short':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            logger.info(
                "/cmd/exposuremode/short")
            # enable overlay in frameserver
            config_instance.CAPTURE_EXPOSURE_MODE = "short"
            frameServer.setAeExposureMode(
                config_instance.CAPTURE_EXPOSURE_MODE)
            self.wfile.write(
                b'/cmd/exposuremode/short\r\n')
        elif self.path == '/cmd/capturePrepare':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            logger.info(
                "imageserver informed about upcoming request to capture")
            # start countdown led and stop autofocus algorithm
            notifier.raise_event("onCountdownTakePicture")
            self.wfile.write(
                b'imageserver informed about upcoming request to capture\r\n')
        elif self.path == '/cmd/infoled/countdown':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            logger.info("request infoLed mode countdown")
            notifier.raise_event("onCountdownTakePicture")
            self.wfile.write(b'Switched capture LED on\r\n')
        elif self.path == '/cmd/autofocus/on':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            logger.info("Switched Autofocus Timer ON")
            rt.start()
            self.wfile.write(b'Switched Autofocus Timer ON\r\n')
        elif self.path == '/cmd/autofocus/off':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            logger.info("Switched Autofocus Timer OFF")
            rt.stop()
            self.wfile.write(b'Switched Autofocus Timer OFF\r\n')
        elif self.path == '/cmd/autofocus/abort':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            logger.info(
                "Aborted autofocus run, returned to previous focus position")
            # focusState.abort()   TODO
            self.wfile.write(
                b'Aborted autofocus run, returned to previous focus position\r\n')
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header(
                'Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    frame = frameServer.wait_for_lores_frame()

                    is_success, buffer = cv2.imencode(
                        ".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, config_instance.LORES_QUALITY])
                    # io_buf = io.BytesIO(buffer)

                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(buffer))
                    self.end_headers()
                    self.wfile.write(buffer)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logger.info(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/capture':
            start_time = time.time()

            content_len = int(self.headers.get('Content-Length', 0))
            post_body = self.rfile.read(content_len)
            logger.debug("post_body(%s)" % (post_body))

            # decode -d "foo=bar" (application/x-www-form-urlencoded) sent by curl like:
            # curl -X POST -d 'filename=%s' http://localhost:8000/capture
            postvars = parse_qs(post_body.decode('utf-8'))
            logger.debug(f"post vars: {postvars}")

            # extract filename
            filename = postvars['filename'][0]
            logger.debug(f"save to file: {filename}")

            try:
                # turn of autofocus trigger, cam needs to be in focus at this point by regular focusing
                rt.stop()

                # triggerpic
                frameServer.trigger_hq_capture()

                # waitforpic and store to disk
                frame = frameServer.wait_for_hq_frame()

                # grab metadata and store to exif
                now = datetime.now()
                zero_ifd = {piexif.ImageIFD.Make: "Arducam",
                            piexif.ImageIFD.Model: picam2.camera.id,
                            piexif.ImageIFD.Software: "Photobooth Imageserver"}
                total_gain = frameServer._metadata["AnalogueGain"] * \
                    frameServer._metadata["DigitalGain"]
                exif_ifd = {piexif.ExifIFD.ExposureTime: (frameServer._metadata["ExposureTime"], 1000000),
                            piexif.ExifIFD.DateTimeOriginal: now.strftime("%Y:%m:%d %H:%M:%S"),
                            piexif.ExifIFD.ISOSpeedRatings: int(total_gain * 100)}

                exif_dict = {"0th": zero_ifd, "Exif": exif_ifd}

                if (locationService.accuracy):
                    logger.info("adding GPS data to exif")
                    logger.debug(
                        f"gps location: {locationService.latitude},{locationService.longitude}")

                    gps_ifd = {
                        piexif.GPSIFD.GPSLatitudeRef: locationService.latitudeRef,
                        piexif.GPSIFD.GPSLatitude: locationService.latitudeDMS,
                        piexif.GPSIFD.GPSLongitudeRef: locationService.longitudeRef,
                        piexif.GPSIFD.GPSLongitude: locationService.longitudeDMS,
                    }
                    # add gps dict
                    exif_dict.update({"GPS": gps_ifd})

                exif_bytes = piexif.dump(exif_dict)

                image = Image.fromarray(frame.astype('uint8'), 'RGB')
                image.save(f"{filename}",
                           quality=config_instance.HIRES_QUALITY, exif=exif_bytes)

                self.send_response(200)
                self.end_headers()
                processing_time = round((time.time() - start_time), 1)
                logger.info(
                    f"capture to file {filename} successfull, process took {processing_time}s")
                self.wfile.write(b'Done, frame capture successful\r\n')
            except Exception as e:
                logger.error(f"error during capture: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f'error during capture: {e}\r\n'.encode())
                self.wfile.write(b'error during capture\r\n')

            finally:
                # turn on regular autofocus in every case
                rt.start()
        else:
            self.send_error(404)
            self.end_headers()


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == '__main__':
    picam2 = Picamera2()
    infoled = InfoLed(config_instance, notifier)
    frameServer = FrameServer(picam2, logger, notifier, config_instance)
    focuser = Focuser(config_instance.FOCUSER_DEVICE, config_instance)
    focusState = FocusState(frameServer, focuser, notifier, config_instance)
    rt = RepeatedTimer(config_instance.FOCUSER_REPEAT_TRIGGER,
                       notifier.raise_event, "onRefocus")
    locationService = LocationService(logger, notifier, config_instance)

    frameServer.start()

    focuser.reset()

    # first time focus
    notifier.raise_event("onRefocus")

    # first time try to get location
    locationService.start()

    # serve files forever
    try:
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        rt.stop()  # better in a try/finally block to make sure the program ends!
        frameServer.stop()
        picam2.stop()
