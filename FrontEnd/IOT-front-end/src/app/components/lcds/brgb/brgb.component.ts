import { HttpClient } from '@angular/common/http';
import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';

@Component({
  selector: 'app-brgb',
  templateUrl: './brgb.component.html',
  styleUrls: ['./brgb.component.css']
})
export class BrgbComponent {
  @Input() lightColor:string = "TURNED OFF";
  @Input() buttonPressed:string="";
  constructor(private http: HttpClient) {}
  
  sendColor(button_pressed: string) {
    this.http.post('http://localhost:5000/button_pressed', { button_pressed: button_pressed })
      .subscribe(response => {
        console.log(response);
      });
  }
  
}
