import { Injectable } from '@angular/core';
import { APIService } from './api.service';
import { Diagnostic } from '../schema';

@Injectable({
  providedIn: 'root'
})
export class DiagnosticService extends APIService<Diagnostic> {
  resource = 'diagnostics';
  sortProperty = ['start_time'];

  parseEntity(record: any): Diagnostic {
    record.start_time = Date.parse(record.start_time);
    record.end_time = Date.parse(record.end_time);
    return record;
  }
}
