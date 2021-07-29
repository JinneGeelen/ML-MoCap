import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { RecordingListComponent } from './page/recording-list/recording-list.component';
import { RecordingCreateComponent } from './page/recording-create/recording-create.component';
import { RecordingDetailsComponent } from './page/recording-details/recording-details.component';

const routes: Routes = [
  {
    path: '',
    redirectTo: 'list',
    pathMatch: 'full'
  },
  {
    path: 'list',
    component: RecordingListComponent
  },
  {
    path: 'new',
    component: RecordingCreateComponent
  },
  {
    path: 'details/:id',
    component: RecordingDetailsComponent
  },
  // Fallback when no prior routes is matched
  { path: '**', redirectTo: 'list', pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class RecordingsRoutingModule { }
