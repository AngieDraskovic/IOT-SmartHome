import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-glcd',
  templateUrl: './glcd.component.html',
  styleUrls: ['./glcd.component.css']
})
export class GlcdComponent {
  @Input() temperature:number = 0;
  @Input() humidity:number = 0;
}
