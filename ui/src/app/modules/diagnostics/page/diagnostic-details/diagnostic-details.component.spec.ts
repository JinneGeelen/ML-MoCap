import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { DiagnosticDetailsComponent } from './diagnostic-details.component';

describe('DiagnosticDetailsComponent', () => {
  let component: DiagnosticDetailsComponent;
  let fixture: ComponentFixture<DiagnosticDetailsComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ DiagnosticDetailsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DiagnosticDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
