import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { DiagnosticCreateComponent } from './diagnostic-create.component';

describe('DiagnosticCreateComponent', () => {
  let component: DiagnosticCreateComponent;
  let fixture: ComponentFixture<DiagnosticCreateComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ DiagnosticCreateComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DiagnosticCreateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
