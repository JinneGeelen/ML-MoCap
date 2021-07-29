import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';

import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { DiagnosticService } from '@data/service/diagnostic.service';
import { DiagnosticResultService } from '@data/service/diagnostic_result.service';
import { Diagnostic, DiagnosticResult } from '@data/schema';

@Component({
  selector: 'app-diagnostic-details',
  templateUrl: './diagnostic-details.component.html',
  styleUrls: ['./diagnostic-details.component.scss']
})
export class DiagnosticDetailsComponent implements OnInit {
  private diagnosticId: string;

  constructor(
    private diagnosticService: DiagnosticService,
    private diagnosticResultService: DiagnosticResultService,
    private router: Router,
    private activeRoute: ActivatedRoute,
  ) {}

  ngOnInit() {
    this.activeRoute.params.subscribe(params => {
      this.diagnosticId = params['id']
      if (this.diagnosticId) {
        this._diagnostic = this.diagnosticService.watch(this.diagnosticId)
      }
    })
  }

  private _diagnostic: Observable<Diagnostic>;
  get diagnostic() {
    return this._diagnostic
  }

  private _results: Observable<DiagnosticResult[]>;
  get results() {
    if (!this._results) {
      this._results = this.diagnosticResultService.watchAll().pipe(
        map(results => {
          return results.filter(result => {
            return result.diagnostic_id === this.diagnosticId;
          })
        })
      );
    }

    return this._results;
  }

  displayedColumns: string[] = [
    'camera_id',
    'iteration',
    'time_start_requested',
    'time_recording_started',
    'delta_sync',
    'delta_recording',
    'delta_start_preview',
    'delta_start_recording',
    'delta_stop_recording',
  ];
}
