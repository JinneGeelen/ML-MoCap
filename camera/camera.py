import io
import asyncio
import os
import logging
import time
import requests
import json
import subprocess
import shutil

from picamera import PiCamera#, PiCameraCircularIO
# from picamera.array import PiMotionAnalysis
from datetime import datetime

logger = logging.getLogger()

# class FrameTimeAnnotator(PiMotionAnalysis):
#     frame_nr = 0

#     def analyze(self, a):
#         # time = datetime.now().strftime(
#         #     '%Y-%m-%d %H:%M:%S.%f')#[:-3]
#         self.frame_nr += 1
#         # self.camera.annotate_text = "frame {} time {}".format(self.frame_nr, time)
#         self.camera.annotate_text = "frame {}".format(self.frame_nr)

#     def reset(self):
#         self.frame_nr = 0

class CameraController():
    camera = None

    recording = False
    diagnostic = False
    recording_base_path = '/home/pi/recordings'

    def get_recording_path(self, recording_id):
        return '{}/{}.h264'.format(self.recording_base_path, recording_id)

    def on_start_recording(self, recording):
        self.stop_uv4l()
        self.camera = PiCamera(
            framerate=30,
            resolution=(640, 480),
        )

        try:
            if self.recording:
                logger.error(
                    'Already recording. Ignoring recording {}...'.format(recording))

            self.diagnostic = None
            if recording.get('is_diagnostic'):
                self.diagnostic = {
                    'diagnostic_id': recording.get('diagnostic_id'),
                    'iteration': recording.get('iteration'),
                    'camera_id': os.environ['ID'],
                    'time_start_requested': recording.get('start_time'),
                    'time_socket_received': datetime.now().astimezone().isoformat(),
                }
                logger.info('Performing diagnostic recording...')

            # self.camera.annotate_text_size = 12
            # # lowering this reduces the motion blur, but makes the video darker
            # self.camera.shutter_speed = 4000
            # # compensate the low shutter speed by increasing the brightness slightly. 50 is the default
            # self.camera.brightness = 55
            # # we compensate the darkening of the image by setting the auto white balance mode to shade
            # self.camera.awb_mode = 'sunlight'

            # motion_output = FrameTimeAnnotator(self.camera)

            # self.camera.start_preview

            # self.camera.start_recording(
            #     '/dev/null',
            #     format='h264',
            #     # the highest available h264 encoding level
            #     level='4.2',
            #     # 10 is the highest, 40 the lowest
            #     quality=15,
            #     # include fps headers in the video
            #     sps_timing=True,
            #     # we set this to 1 so that the split_recording splits on the next frame
            #     intra_period=1,
            #     # this (hopefully) reduces the motion blur
            #     intra_refresh='both',
            #     # embed enhancement information in the frames
            #     sei=True,
            #     # motion_output = motion_output,
            # )
            
            if self.diagnostic:
                self.diagnostic['time_recording_start'] = datetime.now(
                ).astimezone().isoformat()

            # This will loop til the start time of the recording
            start_time = datetime.fromisoformat(recording.get('start_time'))
            logger.info('Waiting until {} to start capturing video...'.format(
                recording.get('start_time')))

            # if self.diagnostic:
            #     self.diagnostic['time_preview_started'] = datetime.now(
            #     ).astimezone().isoformat()

            recording_path = self.get_recording_path(recording.get('id'))
            try:
                os.makedirs(self.recording_base_path)
                os.remove(recording_path)
            except:
                pass

            logger.info('Recording id: {}, with recording path: {}'.format(
                recording.get('id'),recording_path))

            self.recording = True

            current_time = datetime.now().astimezone()
            while current_time < start_time and self.recording:
                time.sleep(0.001)
                current_time = datetime.now().astimezone()

            if self.recording:
                # motion_output.reset()
                # self.camera.split_recording(recording_path)
                
                self.camera.start_recording(recording_path,
                    # '/dev/null',
                    format='h264',
                    # the highest available h264 encoding level
                    level='4.2',
                    # 10 is the highest, 40 the lowest
                    quality=20,
                    # include fps headers in the video
                    sps_timing=True,
                    # we set this to 1 so that the split_recording splits on the next frame
                    # intra_period=1,
                    # this (hopefully) reduces the motion blur
                    # intra_refresh='both',
                    # embed enhancement information in the frames
                    sei=True,
                    # exposure_mode='sports',
                    # motion_output = motion_output,
                )


                if self.diagnostic:
                    self.diagnostic['time_recording_started'] = datetime.now(
                    ).astimezone().isoformat()

                logger.info(
                    'Started capturing video at {}... '.format(datetime.now()))

                while self.recording:
                    self.camera.wait_recording(0.02)

        finally:
            if self.diagnostic:
                self.diagnostic['time_recording_stop'] = datetime.now(
                ).astimezone().isoformat()

            self.camera.stop_recording()

            logger.info(
                'Stopped capturing video at {}... '.format(datetime.now()))

            if self.diagnostic:
                self.diagnostic['time_recording_stopped'] = datetime.now(
                ).astimezone().isoformat()

                logger.info('Sending diagnostic {}'.format(self.diagnostic))
                requests.post(url='http://{}:3000/v1/diagnostic_results/'.format(os.environ['CONTROLLER_HOST']),
                              data=json.dumps(self.diagnostic))

            self.camera.close()
            time.sleep(1)
            #restart uv4l stream
            self.start_uv4l()

    def on_stop_recording(self, recording):
        self.recording = False

    def on_discard_recording(self, recording):
        recording_path = self.get_recording_path(recording.get('id'))
        output_path = recording_path.replace('.h264', '.mp4')
        logger.info('Discard the recording {}'.format(recording_path))

        try:
            os.remove(recording_path)
            os.remove(output_path)
        except:
            pass

    def on_process_recording(self, recording):
        recording_path = self.get_recording_path(recording.get('id'))
        output_path = recording_path.replace('.h264', '.mp4')

        # logger.info('Process the recording from {} to {}'.format(recording_path, output_path))

        try:
            os.remove(output_path)
        except:
            pass

        #ToDo:change! hard-coded fps
        command = "MP4Box -fps 30 -add {} {}".format(
            recording_path, output_path)
        try:
            subprocess.check_output(
                command, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as e:
            logger.error(
                'Error converting h264 to mp4\ncmd: {}\noutput: {}'.format(e.cmd, e.output))
            return

        resp = requests.get(url='http://{}:3000/v1/recordings/{}/storage_path/{}'.format(
            os.environ['CONTROLLER_HOST'],
            recording.get('id'),
            os.environ['ID']
        ))

        if not resp.ok:
            logger.error('Unable to retrieve storage path')
            return

        storage_path = resp.json().get('storage_path')
        logger.info('Uploading video to controller in {}'.format(storage_path))

        command = "scp {} pi@{}:{}".format(
            output_path, os.environ['CONTROLLER_HOST'], storage_path)
        try:
            output = subprocess.check_output(
                command, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as e:
            logger.error(
                'Error copying file to controller {} {}'.format(e.cmd, e.output))
            return

        requests.get(url='http://{}:3000/v1/recordings/{}/processed/{}'.format(
            os.environ['CONTROLLER_HOST'],
            recording.get('id'),
            os.environ['ID']
        ))

        try:
            shutil.rmtree(self.recording_base_path)
        except:
            pass

    async def force_stop(self):
        self.recording = False

    def start_uv4l(self):
        logger.info("Starting uv4l service")
        try:
            subprocess.check_output(
                "sudo systemctl start uv4l_raspicam", stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as e:
            logger.error(
                'Error stopping uv4l service {} {}'.format(e.cmd, e.output))
            return

    def stop_uv4l(self):
        logger.info("Stopping uv4l service")
        try:
            subprocess.check_output(
                "sudo systemctl stop uv4l_raspicam", stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as e:
            logger.error(
                'Error starting uv4l service {} {}'.format(e.cmd, e.output))
            return
