import { Component, Input, SimpleChanges } from '@angular/core';

@Component({
  selector: 'app-covered-porch',
  templateUrl: './covered-porch.component.html',
  styleUrls: ['./covered-porch.component.css']
})
export class CoveredPorchComponent {
  @Input() data: any;
  @Input() lightData:any;
 

}
