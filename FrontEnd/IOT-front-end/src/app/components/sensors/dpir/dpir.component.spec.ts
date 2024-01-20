import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DpirComponent } from './dpir.component';

describe('DpirComponent', () => {
  let component: DpirComponent;
  let fixture: ComponentFixture<DpirComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DpirComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DpirComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
