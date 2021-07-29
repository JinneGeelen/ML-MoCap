import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { StudyListComponent } from './page/study-list/study-list.component';
import { StudyCreateComponent } from './page/study-create/study-create.component';


const routes: Routes = [
  {
    path: '',
    redirectTo: 'list',
    pathMatch: 'full'
  },
  {
    path: 'list',
    component: StudyListComponent
  },

  {
    path: 'new',
    component: StudyCreateComponent
  },
  // Fallback when no prior routes is matched
  { path: '**', redirectTo: 'list', pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class StudiesRoutingModule { }
