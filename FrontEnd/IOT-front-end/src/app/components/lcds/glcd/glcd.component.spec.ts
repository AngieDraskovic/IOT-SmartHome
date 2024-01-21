import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GlcdComponent } from './glcd.component';

describe('GlcdComponent', () => {
  let component: GlcdComponent;
  let fixture: ComponentFixture<GlcdComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GlcdComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GlcdComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
