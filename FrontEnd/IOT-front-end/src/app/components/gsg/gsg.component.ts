import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-gsg',
  templateUrl: './gsg.component.html',
  styleUrls: ['./gsg.component.css']
})
export class GsgComponent {
  @Input() data : number = 0;
}
