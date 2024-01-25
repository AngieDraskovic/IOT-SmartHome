import { Component } from '@angular/core';
import { WebSocketService } from 'src/app/services/web-socket.service';

@Component({
  selector: 'app-alarm-clock',
  templateUrl: './alarm-clock.component.html',
  styleUrls: ['./alarm-clock.component.css']
})
export class AlarmClockComponent {
  time : string = "12:00";
  intervalId : any;
  alarmActive : boolean = false;
  alarmInterval : any;

  constructor(private webSocketService : WebSocketService){

  }

  schedule(){
    if(this.intervalId)
      clearInterval(this.intervalId)
    this.intervalId = setInterval(() => {
      console.log(this.alarmActive  + " EVVOOO GA");
      const currentTime = new Date();
      let currentHours = currentTime.getHours();
      let currentMinutes = currentTime.getMinutes();
      let timeSplit = this.time.split(":")
      if(currentHours == Number.parseInt(timeSplit[0]) && currentMinutes == Number.parseInt(timeSplit[1])){
        if(this.alarmActive)
          return
        console.log("works")
        this.alarmActive = true
        this.webSocketService.sendMessage("alarm_clock_activate", true)
        this.playSound()
      }
    }, 1000)
  }

  playSound(){
    let audio = new Audio();
    audio.src = "../../../assets/audio/alarmClock.WAV";
    audio.load();
    this.alarmInterval = setInterval(() => {
      audio.play();
    }, 3000)
  }



  deactivate(){
    if(this.intervalId)
      clearInterval(this.intervalId)
    this.webSocketService.sendMessage("alarm_clock_deactivate", true)
    clearInterval(this.alarmInterval)
  }
}
