import { Component } from '@angular/core';

@Component({
  selector: 'app-brgb',
  templateUrl: './brgb.component.html',
  styleUrls: ['./brgb.component.css']
})
export class BrgbComponent {
  brightness: number = 50;
  color: string = '#A1A1A1';
  isLightOn: boolean = false;

  togglePower() {
    this.isLightOn = !this.isLightOn;
    console.log('Power state:', this.isLightOn ? 'ON' : 'OFF');
    
  }

  ngOnChanges() {
    console.log(`Brightness: ${this.brightness}, Color: ${this.color}`);
    // ovdje slati na server
  }
}
