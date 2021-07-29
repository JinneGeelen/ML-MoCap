import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ParticipantListComponent } from './page/participant-list/participant-list.component';
import { ParticipantCreateComponent } from './page/participant-create/participant-create.component';


const routes: Routes = [
  {
    path: '',
    redirectTo: 'list',
    pathMatch: 'full'
  },
  {
    path: 'list',
    component: ParticipantListComponent
  },
  {
    path: 'new',
    component: ParticipantCreateComponent
  },
  // Fallback when no prior routes is matched
  { path: '**', redirectTo: 'list', pathMatch: 'full' }
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ParticipantsRoutingModule { }
