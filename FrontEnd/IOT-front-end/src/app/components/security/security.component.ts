import { Component, Input, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import { timeout } from 'rxjs';
import { WebSocketService } from 'src/app/services/web-socket.service';
import { webSocket } from 'rxjs/webSocket';
import { Socket } from 'ngx-socket-io';



@Component({
  selector: 'app-security',
  templateUrl: './security.component.html',
  styleUrls: ['./security.component.css']
})
export class SecurityComponent implements OnInit, OnChanges{
  num1 : string = ""
  num2 : string = ""
  num3 : string = ""
  num4 : string = ""
  currentIndex = -1
  correctCode : string = "1234"
  alarmIsActive : boolean = false;
  @Input() alarmData : any; 
  alarmSystemIsActive : boolean = false;
  @Input() piData : any;
  // socket : any = webSocket('ws://localhost:9001/Key');
  
  constructor(private webSocketService : WebSocketService, private socket : Socket){

  }

  ngOnChanges(changes: SimpleChanges): void {
    if(changes['alarmData'] && changes['alarmData'].currentValue != changes['alarmData'].previousValue){
      console.log(changes)
      this.parseAlarmData(changes['alarmData'].currentValue)
    }
    if(changes['piData'] && this.currentIndex!= -1 && changes['piData'].currentValue != changes['piData'].previousValue)
      this.parseDMS(changes['piData'].currentValue)
  }

  parseAlarmData(value : any){
    this.alarmSystemIsActive = value["system_active"]
    this.alarmIsActive = value["active"]
  }


  ngOnInit(): void {
    this.webSocketService.sendMessage("get_alarm_status", "")
  }

  parseDMS(value : any){
      if(this.currentIndex == 0){
        this.num1 = value
        this.currentIndex += 1
        this.onInput1()
      }
      else if(this.currentIndex == 1){
        this.num2 = value
        this.currentIndex += 1
        this.onInput2()
      }
      else if(this.currentIndex == 2){
        this.num3 = value
        this.currentIndex += 1
        this.onInput3()
      }
      else if(this.currentIndex == 3){
        this.num4 = value
        this.currentIndex = -1
      }
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
    this.webSocketService.sendMessage("activate_alarm_system", fullCode)
    setTimeout(() => {
      this.alarmSystemIsActive = true
    })
  }

  deactivate(){
    let fullCode = this.num1.concat(this.num2, this.num3, this.num4)
    this.webSocketService.sendMessage("deactivate_alarm_system", fullCode)
  }

  verify(){
    let fullCode = this.num1.concat(this.num2, this.num3, this.num4)
    this.webSocketService.sendMessage("input_code", fullCode) 
  }
}
