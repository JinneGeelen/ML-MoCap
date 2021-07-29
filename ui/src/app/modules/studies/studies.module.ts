import { NgModule } from '@angular/core';

import { SharedModule } from '@shared/shared.module';
import { StudiesRoutingModule } from './studies-routing.module';
import { StudyListComponent } from './page/study-list/study-list.component';
import { StudyCreateComponent } from './page/study-create/study-create.component';


@NgModule({
  declarations: [StudyListComponent, StudyCreateComponent],
  imports: [
    SharedModule,
    StudiesRoutingModule
  ]
})
export class StudiesModule { }
