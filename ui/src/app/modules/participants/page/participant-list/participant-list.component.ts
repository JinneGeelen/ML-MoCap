import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { Router, ActivatedRoute } from '@angular/router';
import { ParticipantService } from '@data/service/participant.service';
import { StudyService } from '@data/service/study.service';
import { Participant, Study } from '@data/schema';
import { Observable, combineLatest, of, concat } from 'rxjs';
import { ConfirmationDialogComponent } from '@shared/component/confirmation-dialog/confirmation-dialog.component';
import { map, switchMap } from 'rxjs/operators';
import { MatSelectChange } from '@angular/material/select';

@Component({
  selector: 'app-participant-list',
  templateUrl: './participant-list.component.html',
  styleUrls: ['./participant-list.component.scss']
})
export class ParticipantListComponent implements OnInit {
  public participants$: Observable<Participant[]>;
  public studies$ = this.studyService.watchAll();
  public studyID$ = this.route.paramMap.pipe(
    map(params => {
      return params.get('study') || "";
    })
  );

  public displayedColumns: string[] = [
    'study',
    'number',
    'age',
    'gender',
    'dominant_hand',
    'consent_video',
    'add_recording',
    'delete'
  ];

  constructor(
    private participantService: ParticipantService,
    private studyService: StudyService,
    private router: Router,
    private route: ActivatedRoute,
    public dialog: MatDialog,
  ) { }

  ngOnInit() {
    this.participants$ = combineLatest([
      this.participantService.watchAll(),
      this.studies$,
      this.studyID$,
    ]).pipe(map(([participants, studies, studyID]) => {
      if (studyID.length) {
        participants = participants.filter(participant => {
          return participant.study_id === studyID;
        });
      }

      return participants.map(participant => {
        const study = studies.find(study => {
          return study.id === participant.study_id;
        });

        if (study) {
          participant.study = study;
        }

        return participant;
      });
    }
    ));
  }

  onStudySelect(event: MatSelectChange) {
    if (event.value != null && event.value.length) {
      this.router.navigate(['participants', 'list', { study: event.value }])
    } else {
      this.router.navigate(['participants', 'list'])
    }
  }

  onDeleteClick(event: MouseEvent, row: Participant) {
    event.stopPropagation();
    event.preventDefault();

    const dialogRef = this.dialog.open(ConfirmationDialogComponent, {
      width: '350px',
      data: `Are you sure you want to delete this participant? Note: This will also remove all recordings for this participant.`
    });

    dialogRef.afterClosed().subscribe(async result => {
      if (result) {
        await this.participantService.delete(row.id);
      }
    })
  }

  onAddRecordingClick(event: MouseEvent, row: Participant) {
    event.stopPropagation();
    event.preventDefault();

    this.router.navigate(['recordings', 'new', { participant: row.id }]);
  }

  onRowClick(row: Participant) {
    this.router.navigate(['recordings', 'list', { participant: row.id }]);
  }
}
