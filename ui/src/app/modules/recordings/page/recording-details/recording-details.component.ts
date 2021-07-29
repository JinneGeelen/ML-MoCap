import { Component, OnInit } from '@angular/core';
import { Recording, Camera } from '@data/schema';
import { Observable, combineLatest, interval } from 'rxjs';
import { ActivatedRoute } from '@angular/router';
import { map } from 'rxjs/operators';

import { RecordingService } from '@data/service/recording.service';
import { ParticipantService } from '@data/service/participant.service';
import { StudyService } from '@data/service/study.service';
import { CameraService } from '@data/service/camera.service';

@Component({
  selector: 'app-recording-details',
  templateUrl: './recording-details.component.html',
  styleUrls: ['./recording-details.component.scss']
})
export class RecordingDetailsComponent implements OnInit {
  public recording$: Observable<Recording>;
  public recordingState$: Observable<string>;

  public cameras$: Observable<Camera[]>;
  public participants$ = this.participantService.watchAll();
  public studies$ = this.studyService.watchAll();

  public recordingButtonText$: Observable<String>;

  private requestedStartTime: number;

  private get recordingID() {
    return this.route.snapshot.paramMap.get('id');
  }

  constructor(
    private recordingService: RecordingService,
    private participantService: ParticipantService,
    private studyService: StudyService,
    private cameraService: CameraService,
    private route: ActivatedRoute,
  ) { }

  ngOnInit() {
    this.recording$ = combineLatest([
      this.recordingService.watchAll(),
      this.participants$,
      this.studies$,
      this.route.paramMap.pipe(
        map(params => {
          return params.get('id');
        })
      )
    ])
      .pipe(map(([recordings, participants, studies, recordingID]) => {
        if (!recordings.length) {
          return null;
        }

        const recording = recordings.find(recording => {
          return recording.id === recordingID;
        });

        if (!recording) {
          return null;
        }

        recording.participant = participants.find(participant => {
          return participant.id === recording.participant_id;
        });

        if (recording.participant) {
          recording.participant.study = studies.find(study => {
            return study.id === recording.participant.study_id;
          });
        }

        return recording
      }));

    this.cameras$ = combineLatest([
      this.cameraService.watchAll(),
      this.recording$
    ]).pipe(map(([cameras, recording]) => {
      return cameras.map(camera => {
        switch (recording && recording.state) {
          case 'empty':
            window.URL.revokeObjectURL(this.getStreamUrl(camera));
            camera.state = 'streaming';
            break;
          case 'recording':
            camera.state = 'recording';
            break;
          case 'unprocessed':
            camera.state = 'unprocessed';
            break;
          case 'processed':
            camera.state = 'processed';
            break;
          case 'processing':
            if (recording.cameras_processing.includes(camera.id)) {
              camera.state = 'processing';
            }
            else if (recording.cameras_processed.includes(camera.id)) {
              camera.state = 'processed';
            }
            break;
        }

        return camera;
      });
    }));

    this.recording$.subscribe((recording) => {
      if (recording && recording.state == "recording") {
        this.requestedStartTime = Date.parse(recording.start_time);
        this.recordingButtonText$ = interval(50).pipe(map(() => {
          const now = Date.now();
          if (this.requestedStartTime > now) {
            return Math.ceil((this.requestedStartTime - now) / 1000).toString();
          }
          return "Stop";
        }))
      } else {
        this.requestedStartTime = 0;
        this.recordingButtonText$ = null;
      }
    });
  }

  public getStreamUrl(camera: Camera) {
    return 'http://' + camera.id + '.local:8080/stream/video.mjpeg';
  }

  public async onStartClick() {
    await this.recordingService.start(this.recordingID);
  }

  public async onStopClick() {
    if (Date.now() > this.requestedStartTime) {
      await this.recordingService.stop(this.recordingID);
    }
  }

  public async onDiscardClick() {
    await this.recordingService.discard(this.recordingID);
  }

  public async onSaveClick() {
    await this.recordingService.process(this.recordingID);
  }
}
