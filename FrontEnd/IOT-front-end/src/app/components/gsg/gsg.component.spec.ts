import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GsgComponent } from './gsg.component';

describe('GsgComponent', () => {
  let component: GsgComponent;
  let fixture: ComponentFixture<GsgComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GsgComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GsgComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
