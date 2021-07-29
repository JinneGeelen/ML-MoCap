import { Injectable } from '@angular/core';
import { APIService } from './api.service';
import { Camera } from '../schema';

@Injectable({
  providedIn: 'root'
})
export class CameraService extends APIService<Camera> {
  resource = 'cameras';
}
