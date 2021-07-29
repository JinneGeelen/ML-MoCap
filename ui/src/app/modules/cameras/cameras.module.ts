import { NgModule } from '@angular/core';

import { CamerasRoutingModule } from './cameras-routing.module';
import { CameraListComponent } from './page/camera-list/camera-list.component';
import { SharedModule } from '@shared/shared.module';

@NgModule({
  declarations: [
    CameraListComponent
  ],
  imports: [
    SharedModule,
    CamerasRoutingModule
  ]
})
export class CamerasModule { }
