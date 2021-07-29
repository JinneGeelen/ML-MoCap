import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { DiagnosticListComponent } from './diagnostic-list.component';

describe('DiagnosticsListComponent', () => {
  let component: DiagnosticListComponent;
  let fixture: ComponentFixture<DiagnosticListComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ DiagnosticListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DiagnosticListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
