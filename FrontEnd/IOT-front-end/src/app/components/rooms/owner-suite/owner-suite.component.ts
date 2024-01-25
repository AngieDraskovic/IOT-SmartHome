import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-owner-suite',
  templateUrl: './owner-suite.component.html',
  styleUrls: ['./owner-suite.component.css']
})
export class OwnerSuiteComponent {
  @Input() timeData: any;
  @Input() colorData: any;
  @Input() buttonPressedData:any;
  @Input() alarmActive : boolean = false;
  
}
