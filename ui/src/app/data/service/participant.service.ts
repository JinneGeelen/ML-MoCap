import { Injectable } from '@angular/core';
import { APIService } from './api.service';
import { Participant } from '../schema';

@Injectable({
  providedIn: 'root'
})
export class ParticipantService extends APIService<Participant> {
  resource = 'participants';
}
