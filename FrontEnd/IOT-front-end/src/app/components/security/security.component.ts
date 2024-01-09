import { Component, OnInit } from '@angular/core';
import { IMqttMessage, MqttService } from 'ngx-mqtt';


@Component({
  selector: 'app-security',
  templateUrl: './security.component.html',
  styleUrls: ['./security.component.css']
})
export class SecurityComponent implements OnInit{
  num1 : String = ""
  num2 : String = ""
  num3 : String = ""
  num4 : String = ""
  currentIndex = 0
  correctCode : String = "1234"
  alarmIsActive : boolean = false;
  
  constructor(private mqttService : MqttService){

  }

  ngOnInit(): void {
    this.mqttService.observe('Key').subscribe((message : IMqttMessage) => {
      let payload = JSON.parse(message.payload.toString())
      if(this.currentIndex == 0){
        this.num1 = payload.value
        this.onInput1()
      }
      else if(this.currentIndex == 1){
        this.num2 = payload.value
        this.onInput2()
      }
      else if(this.currentIndex == 2){
        this.num3 = payload.value
        this.onInput3()
      }
      else if(this.currentIndex == 3){
        this.num4 = payload.value
        this.currentIndex = -1
      }
    });
  }

  onInput1(){
    document.getElementById('input2')?.focus();
    this.currentIndex += 1
  }
  
  onInput2(){
    document.getElementById('input3')?.focus();
    this.currentIndex += 1
  }
  
  onInput3(){
    document.getElementById('input4')?.focus();
    this.currentIndex += 1
  }

  generateCode(){
    this.currentIndex = 0
  }
}
