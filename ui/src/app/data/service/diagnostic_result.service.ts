import { Injectable } from '@angular/core';
import { APIService } from './api.service';
import { DiagnosticResult } from '../schema';

@Injectable({
  providedIn: 'root'
})
export class DiagnosticResultService extends APIService<DiagnosticResult> {
  resource = 'diagnostic_results';
  sortProperty = ['iteration', 'camera_id'];

  parseEntity(record: any): DiagnosticResult {
    record.time_start_requested = Date.parse(record.time_start_requested);
    record.time_socket_received = Date.parse(record.time_socket_received);
    record.time_preview_started = Date.parse(record.time_preview_started);
    record.time_recording_start = Date.parse(record.time_recording_start);
    record.time_recording_started = Date.parse(record.time_recording_started);
    record.time_recording_stop = Date.parse(record.time_recording_stop);
    record.time_recording_stopped = Date.parse(record.time_recording_stopped);
    return record;
  }
}
