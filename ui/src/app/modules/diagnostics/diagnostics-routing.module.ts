import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { DiagnosticListComponent } from './page/diagnostic-list/diagnostic-list.component';
import { DiagnosticCreateComponent } from './page/diagnostic-create/diagnostic-create.component';
import { DiagnosticDetailsComponent } from './page/diagnostic-details/diagnostic-details.component';


const routes: Routes = [
  {
    path: '',
    component: DiagnosticListComponent
  },
  {
    path: 'new',
    component: DiagnosticCreateComponent
  },
  {
    path: 'details/:id',
    component: DiagnosticDetailsComponent
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class DiagnosticsRoutingModule { }
