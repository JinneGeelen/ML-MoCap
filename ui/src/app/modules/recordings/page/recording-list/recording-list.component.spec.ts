import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { RecordingListComponent } from './recording-list.component';

describe('RecordingsListComponent', () => {
  let component: RecordingListComponent;
  let fixture: ComponentFixture<RecordingListComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ RecordingListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RecordingListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
