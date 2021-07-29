import { Component } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { StudyService } from '@data/service/study.service';
import { Study } from '@data/schema';
import { Router } from '@angular/router';

@Component({
  selector: 'app-study-create',
  templateUrl: './study-create.component.html',
  styleUrls: ['./study-create.component.scss']
})
export class StudyCreateComponent {
  public studyForm = this.fb.group({
    name: "",
    researcher: "Jinne Geelen",
    date: `${(new Date()).getMonth()+1}-${(new Date()).getFullYear()}`,
    emg: false,
  });;

  constructor(
    private studyService: StudyService,
    private fb: FormBuilder,
    private router: Router
  ) {}

  async onSubmit(studyData: Study) {
    const study = await this.studyService.create(studyData);
    this.router.navigate(['participants', 'new', study.id])
  }
}
