import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OwnerSuiteComponent } from './owner-suite.component';

describe('OwnerSuiteComponent', () => {
  let component: OwnerSuiteComponent;
  let fixture: ComponentFixture<OwnerSuiteComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ OwnerSuiteComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(OwnerSuiteComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
