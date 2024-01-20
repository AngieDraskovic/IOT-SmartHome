import { Component, OnInit } from '@angular/core';
import { IMqttMessage, MqttService } from 'ngx-mqtt';
import { timeout } from 'rxjs';


@Component({
  selector: 'app-security',
  templateUrl: './security.component.html',
  styleUrls: ['./security.component.css']
})
export class SecurityComponent implements OnInit{
  num1 : string = ""
  num2 : string = ""
  num3 : string = ""
  num4 : string = ""
  currentIndex = -1
  correctCode : string = "1234"
  alarmIsActive : boolean = false;
  
  constructor(private mqttService : MqttService){

  }

  ngOnInit(): void {
    this.mqttService.observe('Key').subscribe((message : IMqttMessage) => {
      this.parseDMS(message)
    });
    this.mqttService.observe('Door Status').subscribe((message : IMqttMessage) => {
      this.parseDS(message)
    });
  }

  parseDMS(message : IMqttMessage){
    console.log(message.payload.toString())
    let payload = JSON.parse(message.payload.toString())
      if(this.currentIndex == 0){
        this.num1 = payload.value
        this.currentIndex += 1
        this.onInput1()
      }
      else if(this.currentIndex == 1){
        this.num2 = payload.value
        this.currentIndex += 1
        this.onInput2()
      }
      else if(this.currentIndex == 2){
        this.num3 = payload.value
        this.currentIndex += 1
        this.onInput3()
      }
      else if(this.currentIndex == 3){
        this.num4 = payload.value
        this.currentIndex = -1
      }
  }

  parseDS(message : IMqttMessage){
    let payload = JSON.parse(message.payload.toString())
  }

  onInput1(){
    document.getElementById('input2')?.focus();
  }
  
  onInput2(){
    document.getElementById('input3')?.focus();
  }
  
  onInput3(){
    document.getElementById('input4')?.focus();
  }

  generateCode(){
    this.currentIndex = 0
  }

  activate(){
    let fullCode = this.num1.concat(this.num2, this.num3, this.num4)
    setTimeout(() => {
      this.alarmIsActive = true
    })
  }
}
