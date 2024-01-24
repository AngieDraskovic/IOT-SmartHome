import { Component, Input, SimpleChanges } from '@angular/core';

@Component({
  selector: 'app-ds',
  templateUrl: './ds.component.html',
  styleUrls: ['./ds.component.css']
})
export class DsComponent {
 
  @Input() door_opened:string = "closed";
  

  ngOnChanges(changes: SimpleChanges): void {
    console.log(this.door_opened)
  }

  
}
