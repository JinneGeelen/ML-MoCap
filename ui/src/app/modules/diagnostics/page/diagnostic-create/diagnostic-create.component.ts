import { Component } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { DiagnosticService } from '@data/service/diagnostic.service';
import { Diagnostic } from '@data/schema';
import { Router } from '@angular/router';

@Component({
  selector: 'app-diagnostic-create',
  templateUrl: './diagnostic-create.component.html',
  styleUrls: ['./diagnostic-create.component.scss']
})
export class DiagnosticCreateComponent {
  public diagnosticForm = this.fb.group({
    iterations: 10
  });;

  constructor(
    private diagnosticService: DiagnosticService,
    private fb: FormBuilder,
    private router: Router
  ) {}

  async onSubmit(diagnosticData: Diagnostic) {
    const diagnostic = await this.diagnosticService.create(diagnosticData);

    this.diagnosticForm.reset({
      iterations: 10
    });

    this.router.navigate(['diagnostics', 'details', diagnostic.id])
  }
}
