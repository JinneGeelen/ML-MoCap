import { Component } from '@angular/core';
import { StudyService } from '@data/service/study.service';
import { Observable } from 'rxjs';
import { Study } from '@data/schema';
import { Router } from '@angular/router';
import { MatDialog } from '@angular/material/dialog';
import { ConfirmationDialogComponent } from '@shared/component/confirmation-dialog/confirmation-dialog.component';

@Component({
  selector: 'app-study-list',
  templateUrl: './study-list.component.html',
  styleUrls: ['./study-list.component.scss']
})
export class StudyListComponent {
  constructor(
    private studyService: StudyService,
    private router: Router,
    public dialog: MatDialog,
  ) {}

  private _studies: Observable<Study[]>;
  get studies() {
    if (!this._studies) {
      this._studies = this.studyService.watchAll();
    }

    return this._studies;
  }

  displayedColumns: string[] = [
    'name',
    'researcher',
    'date',
    'emg',
    'add_participant',
    'delete'
  ];

  onDeleteClick(event: MouseEvent, row: Study) {
    event.stopPropagation();
    event.preventDefault();

    const dialogRef = this.dialog.open(ConfirmationDialogComponent, {
      width: '350px',
      data: `Are you sure you want to delete this study? Note: This will also remove all recordings for this study.`
    });

    dialogRef.afterClosed().subscribe(async result => {
      if (result) {
        await this.studyService.delete(row.id);
      }
    })
  }

  onAddParticipantClick(event: MouseEvent, row: Study) {
    event.stopPropagation();
    event.preventDefault();

    this.router.navigate(['participants', 'new', {study: row.id}])
  }

  onRowClick(row: Study) {
    this.router.navigate(['participants', 'list', {study: row.id}]);
  }
}
