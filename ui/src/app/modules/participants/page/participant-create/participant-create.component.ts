import { Component, OnInit, OnDestroy } from '@angular/core';
import { ParticipantService } from '@data/service/participant.service';
import { Participant, Study } from '@data/schema';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder } from '@angular/forms';
import { Observable, Subject } from 'rxjs';
import { StudyService } from '@data/service/study.service';
import { map, takeUntil } from 'rxjs/operators';

@Component({
  selector: 'app-participant-create',
  templateUrl: './participant-create.component.html',
  styleUrls: ['./participant-create.component.scss']
})
export class ParticipantCreateComponent implements OnInit, OnDestroy {
  public studies$ = this.studyService.watchAll();
  private unsubscribe: Subject<void> = new Subject();

  public participantForm = this.fb.group({
    study_id: '',
    number: '',
    age: 25,
    dominant_hand: 'Right',
    gender: 'Female',
    consent_video: false,
  });;

  constructor(
    private participantService: ParticipantService,
    private studyService: StudyService,
    private fb: FormBuilder,
    private router: Router,
    private route: ActivatedRoute,
  ) {}

  ngOnInit() {
    this.route.paramMap
      .pipe(
        takeUntil(this.unsubscribe),
        map(params => {
          return params.get('study') || '';
        })
      )
      .subscribe(studyID => {
        if (studyID.length) {
          this.participantForm.patchValue({
            study_id: studyID
          });
          this.participantForm.get('study_id').disable();
        }
      });
  }

  ngOnDestroy() {
    this.unsubscribe.next();
    this.unsubscribe.complete();
  }

  async onSubmit() {
    const data = this.participantForm.getRawValue();
    const participant = await this.participantService.create(data);
    this.router.navigate(['recordings', 'new', {participant: participant.id}])
  }
}
