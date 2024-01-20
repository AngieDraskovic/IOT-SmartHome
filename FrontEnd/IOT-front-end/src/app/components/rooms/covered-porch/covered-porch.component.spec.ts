import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CoveredPorchComponent } from './covered-porch.component';

describe('CoveredPorchComponent', () => {
  let component: CoveredPorchComponent;
  let fixture: ComponentFixture<CoveredPorchComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CoveredPorchComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CoveredPorchComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
