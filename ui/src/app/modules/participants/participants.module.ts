import { NgModule } from '@angular/core';

import { ParticipantsRoutingModule } from './participants-routing.module';
import { ParticipantListComponent } from './page/participant-list/participant-list.component';
import { ParticipantCreateComponent } from './page/participant-create/participant-create.component';
import { SharedModule } from '@shared/shared.module';


@NgModule({
  declarations: [ParticipantListComponent, ParticipantCreateComponent],
  imports: [
    SharedModule,
    ParticipantsRoutingModule
  ]
})
export class ParticipantsModule { }
