import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DLComponent } from './dl.component';

describe('DLComponent', () => {
  let component: DLComponent;
  let fixture: ComponentFixture<DLComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DLComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DLComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
