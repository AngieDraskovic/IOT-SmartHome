import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-b4sd',
  templateUrl: './b4sd.component.html',
  styleUrls: ['./b4sd.component.css']
})
export class B4sdComponent {
  @Input() time:string ="08:00";
}
