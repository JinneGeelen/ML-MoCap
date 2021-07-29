import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { CameraListComponent } from '@modules/cameras/page/camera-list/camera-list.component';


const routes: Routes = [
  {
    path: '',
    component: CameraListComponent
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CamerasRoutingModule { }
