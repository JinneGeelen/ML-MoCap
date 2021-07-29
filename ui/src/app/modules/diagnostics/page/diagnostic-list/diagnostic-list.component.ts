import { Component } from '@angular/core';
import { DiagnosticService } from '@data/service/diagnostic.service';
import { Observable } from 'rxjs';
import { Diagnostic } from '@data/schema';
import { Router } from '@angular/router';

@Component({
  selector: 'app-diagnostic-list',
  templateUrl: './diagnostic-list.component.html',
  styleUrls: ['./diagnostic-list.component.scss']
})
export class DiagnosticListComponent {
  constructor(private diagnosticService: DiagnosticService,
              private router: Router) {}

  private _diagnostics: Observable<Diagnostic[]>
  get diagnostics() {
    if (!this._diagnostics) {
      this._diagnostics = this.diagnosticService.watchAll();
    }

    return this._diagnostics;
  }

  displayedColumns: string[] = ['start_time', 'end_time', 'iterations'];

  onRowClick(row: Diagnostic) {
    this.router.navigate(['diagnostics', 'details', row.id]);
  }
}
