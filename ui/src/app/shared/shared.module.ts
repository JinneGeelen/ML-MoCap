import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { ControlMessagesComponent } from './component/control-messages/control-messages.component';
import { MaterialModule } from './material.module';
import { ConfirmationDialogComponent } from './component/confirmation-dialog/confirmation-dialog.component';

@NgModule({
  imports: [CommonModule, MaterialModule, FormsModule, ReactiveFormsModule, RouterModule],
  declarations: [ControlMessagesComponent, ConfirmationDialogComponent],
  entryComponents: [ConfirmationDialogComponent],
  exports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    RouterModule,
    MaterialModule,
    ControlMessagesComponent
  ]
})
export class SharedModule {}
