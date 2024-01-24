import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BrgbComponent } from './brgb.component';

describe('BrgbComponent', () => {
  let component: BrgbComponent;
  let fixture: ComponentFixture<BrgbComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BrgbComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(BrgbComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
