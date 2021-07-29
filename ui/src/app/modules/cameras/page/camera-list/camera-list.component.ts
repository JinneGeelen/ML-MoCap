import { Component, OnInit } from '@angular/core';
import { CameraService } from '@data/service/camera.service';
import { Observable } from 'rxjs';
import { Camera } from '@data/schema';

@Component({
  selector: 'app-camera-list',
  templateUrl: './camera-list.component.html',
  styleUrls: ['./camera-list.component.scss']
})
export class CameraListComponent {
  constructor(private cameraService: CameraService) {}

  private _cameras: Observable<Camera[]>
  get cameras$() {
    if (!this._cameras) {
      this._cameras = this.cameraService.watchAll();
    }

    return this._cameras;
  }
}
