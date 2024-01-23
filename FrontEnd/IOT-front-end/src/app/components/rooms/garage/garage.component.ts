import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-garage',
  templateUrl: './garage.component.html',
  styleUrls: ['./garage.component.css']
})
export class GarageComponent {
  @Input() data: any;
  @Input() doorSensorData: any;
}
