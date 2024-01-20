import { Component, OnInit } from '@angular/core';
import { IMqttMessage, IMqttServiceOptions, MqttService } from 'ngx-mqtt';
import { Subscription } from 'rxjs';


@Component({
  selector: 'app-dpir',
  templateUrl: './dpir.component.html',
  styleUrls: ['./dpir.component.css']
})
export class DpirComponent implements OnInit{
  

  constructor(private mqttService: MqttService) {
  
  }

  ngOnInit():void{
    this.mqttService.observe('frontend/update').subscribe((message: IMqttMessage) => {
      console.log("cao");
      const messageData = JSON.parse(message.payload.toString());
      console.log(messageData);
      // Ovde implementirajte logiku za obradu poruka
    });
  }

}
