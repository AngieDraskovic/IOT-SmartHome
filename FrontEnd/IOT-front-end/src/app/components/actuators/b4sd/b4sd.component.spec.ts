import { ComponentFixture, TestBed } from '@angular/core/testing';

import { B4sdComponent } from './b4sd.component';

describe('B4sdComponent', () => {
  let component: B4sdComponent;
  let fixture: ComponentFixture<B4sdComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ B4sdComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(B4sdComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
