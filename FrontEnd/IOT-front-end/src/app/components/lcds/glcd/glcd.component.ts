import { Component } from '@angular/core';

@Component({
  selector: 'app-glcd',
  templateUrl: './glcd.component.html',
  styleUrls: ['./glcd.component.css']
})
export class GlcdComponent {
  temperature:number = 0;
  humidity:number = 0;
}
