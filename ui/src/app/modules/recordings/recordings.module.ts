import { NgModule } from '@angular/core';

import { RecordingsRoutingModule } from './recordings-routing.module';
import { RecordingListComponent } from './page/recording-list/recording-list.component';
import { SharedModule } from '@shared/shared.module';
import { RecordingCreateComponent } from './page/recording-create/recording-create.component';
import { RecordingDetailsComponent } from './page/recording-details/recording-details.component';

@NgModule({
  declarations: [RecordingListComponent, RecordingCreateComponent, RecordingDetailsComponent], 
  imports: [
    SharedModule,
    RecordingsRoutingModule
  ]
})
export class RecordingsModule { }
