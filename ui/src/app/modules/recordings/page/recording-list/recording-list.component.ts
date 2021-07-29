import { Component, OnInit } from '@angular/core';
import { RecordingService } from '@data/service/recording.service';
import { Observable, combineLatest } from 'rxjs';
import { Recording } from '@data/schema';
import { Router, ActivatedRoute } from '@angular/router';
import { MatDialog } from '@angular/material/dialog';
import { ConfirmationDialogComponent } from '@shared/component/confirmation-dialog/confirmation-dialog.component';
import { ParticipantService } from '@data/service/participant.service';
import { map } from 'rxjs/operators';
import { MatSelectChange } from '@angular/material/select';

@Component({
  selector: 'app-recording-list',
  templateUrl: './recording-list.component.html',
  styleUrls: ['./recording-list.component.scss']
})
export class RecordingListComponent implements OnInit {
  public recordings$: Observable<Recording[]>;
  public participants$ = this.participantService.watchAll();
  public participantID$ = this.route.paramMap.pipe(
    map(params => {
      return params.get('participant') || "";
    })
  );

  displayedColumns: string[] = [
    'name',
    'participant',
    'start_time',
    'end_time',
    'delete'
  ];

  constructor(
    private recordingService: RecordingService,
    private participantService: ParticipantService,
    private router: Router,
    private route: ActivatedRoute,
    public dialog: MatDialog,
  ) { }

  ngOnInit() {
    this.recordings$ = combineLatest([
      this.recordingService.watchAll(),
      this.participants$,
      this.participantID$
    ]).pipe(map(([recordings, participants, participantID]) => {
      if (participantID.length) {
        recordings = recordings.filter(recording => {
          return recording.participant_id === participantID;
        });
      }

      return recordings.map(recording => {
        const participant = participants.find(participant => {
          return participant.id === recording.participant_id;
        });

        if (participant) {
          recording.participant = participant;
        }

        return recording;
      });
    }));
  }

  onParticipantSelect(event: MatSelectChange) {
    if (event.value != null && event.value.length) {
      this.router.navigate(['recordings', 'list', { participant: event.value }])
    } else {
      this.router.navigate(['recordings', 'list'])
    }
  }

  onDeleteClick(event: MouseEvent, row: Recording) {
    event.stopPropagation();
    event.preventDefault();

    const dialogRef = this.dialog.open(ConfirmationDialogComponent, {
      width: '350px',
      data: `Are you sure you want to delete this recording? Note: This will remove the recordings of all cameras for this recording.`
    });

    dialogRef.afterClosed().subscribe(async result => {
      if (result) {
        await this.recordingService.delete(row.id);
      }
    })
  }

  onRowClick(row: Recording) {
    this.router.navigate(['recordings', 'details', row.id]);
  }
}
