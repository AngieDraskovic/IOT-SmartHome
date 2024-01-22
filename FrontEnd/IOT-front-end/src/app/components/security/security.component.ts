import { Component, OnInit } from '@angular/core';
import { timeout } from 'rxjs';
import { WebSocketService } from 'src/app/services/web-socket.service';
import { webSocket } from 'rxjs/webSocket';
import { Socket } from 'ngx-socket-io';



@Component({
  selector: 'app-security',
  templateUrl: './security.component.html',
  styleUrls: ['./security.component.css']
})
export class SecurityComponent{
  num1 : string = ""
  num2 : string = ""
  num3 : string = ""
  num4 : string = ""
  currentIndex = -1
  correctCode : string = "1234"
  alarmIsActive : boolean = false;
  // socket : any = webSocket('ws://localhost:9001/Key');
  
  constructor(private webSocketService : WebSocketService, private socket : Socket){

  }


  ngOnInit(): void {
    this.webSocketService.getMessage().subscribe(data => {
      console.log(data)
    })
  }

  parseDMS(message : any){
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
    console.log("testing")
    this.webSocketService.sendMessage("testing")
    this.currentIndex = 0
  }

  activate(){
    let fullCode = this.num1.concat(this.num2, this.num3, this.num4)
    setTimeout(() => {
      this.alarmIsActive = true
    })
  }
}
