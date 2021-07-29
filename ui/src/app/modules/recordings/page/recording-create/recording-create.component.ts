import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { RecordingService } from '@data/service/recording.service';
import { Recording } from '@data/schema';
import { Router, ActivatedRoute } from '@angular/router';
// import { StudyService } from '@data/service/study.service';
import { ParticipantService } from '@data/service/participant.service';
import { Subject } from 'rxjs';
import { takeUntil, map } from 'rxjs/operators';

@Component({
  selector: 'app-recording-create',
  templateUrl: './recording-create.component.html',
  styleUrls: ['./recording-create.component.scss']
})
export class RecordingCreateComponent implements OnInit, OnDestroy {
  private unsubscribe: Subject<void> = new Subject();

  // // TODO add studies to selection, default option show only participant from selected/latest study
  // public studies$ = this.studyService.watchAll();

  public participants$ = this.participantService.watchAll();

  public recordingForm = this.fb.group({
    name: `${(new Date()).getDate()}-${(new Date()).getMonth()+1}-${(new Date()).getFullYear()} ${(new Date()).getHours()}:${(new Date()).getMinutes()}`,
    participant_id: ''
  });;

  constructor(
    private recordingService: RecordingService,
    private participantService: ParticipantService,
    private fb: FormBuilder,
    private router: Router,
    private route: ActivatedRoute,
  ) {}

  ngOnInit() {
    this.route.paramMap
      .pipe(
        takeUntil(this.unsubscribe),
        map(params => {
          return params.get('participant') || '';
        })
      )
      .subscribe(participantID => {
        if (participantID.length) {
          this.recordingForm.patchValue({
            participant_id: participantID
          });
          this.recordingForm.get('participant_id').disable();
        }
      });
  }

  ngOnDestroy() {
    this.unsubscribe.next();
    this.unsubscribe.complete();
  }

  async onSubmit() {
    const data = this.recordingForm.getRawValue();
    const recording = await this.recordingService.create(data);
    this.router.navigate(['recordings', 'details', recording.id])
  }
}
