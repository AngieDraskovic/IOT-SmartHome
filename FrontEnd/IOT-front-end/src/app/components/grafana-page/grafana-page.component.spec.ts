import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GrafanaPageComponent } from './grafana-page.component';

describe('GrafanaPageComponent', () => {
  let component: GrafanaPageComponent;
  let fixture: ComponentFixture<GrafanaPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GrafanaPageComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GrafanaPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
