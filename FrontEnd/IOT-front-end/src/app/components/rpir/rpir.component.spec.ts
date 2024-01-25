import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RpirComponent } from './rpir.component';

describe('RpirComponent', () => {
  let component: RpirComponent;
  let fixture: ComponentFixture<RpirComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RpirComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RpirComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
