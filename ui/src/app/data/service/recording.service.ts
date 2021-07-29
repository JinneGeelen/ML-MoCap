import { Injectable } from '@angular/core';
import { APIService } from './api.service';
import { Recording } from '../schema';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class RecordingService extends APIService<Recording> {
  resource = 'recordings';

  public async start(id: string): Promise<Recording> {
    return await <Promise<Recording>>this.http.get(`${this.resourceUrl}${id}/start`).toPromise();
  }

  public async stop(id: string): Promise<Recording> {
    return await <Promise<Recording>>this.http.get(`${this.resourceUrl}${id}/stop`).toPromise();
  }

  public async discard(id: string): Promise<Recording> {
    return await <Promise<Recording>>this.http.get(`${this.resourceUrl}${id}/discard`).toPromise();
  }

  public async process(id: string): Promise<Recording> {
    return await <Promise<Recording>>this.http.get(`${this.resourceUrl}${id}/process`).toPromise();
  }
}
