import { NgModule } from '@angular/core';

import { DiagnosticsRoutingModule } from './diagnostics-routing.module';
import { SharedModule } from '@shared/shared.module';
import { DiagnosticListComponent } from './page/diagnostic-list/diagnostic-list.component';
import { DiagnosticCreateComponent } from './page/diagnostic-create/diagnostic-create.component';
import { DiagnosticDetailsComponent } from './page/diagnostic-details/diagnostic-details.component';


@NgModule({
  declarations: [DiagnosticListComponent, DiagnosticCreateComponent, DiagnosticDetailsComponent],
  imports: [
    SharedModule,
    DiagnosticsRoutingModule
  ]
})
export class DiagnosticsModule { }
