import { Injectable } from '@angular/core';
import { APIService } from './api.service';
import { Study } from '../schema';

@Injectable({
  providedIn: 'root'
})
export class StudyService extends APIService<Study> {
  resource = 'studies';
}
