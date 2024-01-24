import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';

@Component({
  selector: 'app-dl',
  templateUrl: './dl.component.html',
  styleUrls: ['./dl.component.css']
})
export class DLComponent implements OnChanges{

  @Input() lightOn:boolean = false;
  bulbSrc: string = 'https://i.postimg.cc/KjK1wL3c/bulb-off.png'; 

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['lightOn']) {
      if (this.lightOn) {
        this.bulbSrc = 'https://i.postimg.cc/6QyTynzr/bulb-on.png';
      } else {
        this.bulbSrc = 'https://i.postimg.cc/KjK1wL3c/bulb-off.png';
      }
    }
  }
}
