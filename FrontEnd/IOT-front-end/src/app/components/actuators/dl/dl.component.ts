import { Component } from '@angular/core';

@Component({
  selector: 'app-dl',
  templateUrl: './dl.component.html',
  styleUrls: ['./dl.component.css']
})
export class DLComponent {
  bulbSrc: string = 'https://i.postimg.cc/KjK1wL3c/bulb-off.png'; 
  bulbOn(): void {
    const bulbElement = document.getElementById('bulb') as HTMLImageElement;
    if (bulbElement) {
      bulbElement.src = 'https://i.postimg.cc/6QyTynzr/bulb-on.png'; // URL slike sijalice koja je uključena
    }
  }

  bulbOff(): void {
    const bulbElement = document.getElementById('bulb') as HTMLImageElement;
    if (bulbElement) {
      bulbElement.src = 'https://i.postimg.cc/KjK1wL3c/bulb-off.png'; // URL slike sijalice koja je isključena
    }
  }
}
