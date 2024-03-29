import { Component, OnInit, Output } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { WebSocketService } from 'src/app/services/web-socket.service';
import { MatDialog } from '@angular/material/dialog';
import { AlarmComponent } from '../alarm/alarm.component';
import { AlarmDataService } from 'src/app/services/alarm-data.service';

@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.css']
})
export class HomePageComponent implements OnInit{
  constructor(private webSocketService: WebSocketService, 
    private socket: Socket,
    public dialog: MatDialog,
    private alarmDataService: AlarmDataService) { }
  coveredPorchData: any;
  lightData:any;        // ide i on za coveredPorch ali je drugaciji child pa sam ovako
  garageData:any;

  doorSensorCPdata:any; // takodje za covered porch
  doorSensorGdata:any; // za garazu 
  dmsData:any;
  dmsLoadingData : any;
  rpirData : any;
  gsgData : any
  isAlarmActive = false;
  alarmDialogRef: any; 
  temperature : number = 0;
  humidity : number = 0;

  alarmInterval : any;

  timeData:any;
  colorData:any;
  buttonPressedData:any;
  ngOnInit(): void {
    this.webSocketService.getMessage().subscribe(data => {
      this.handleData(data)
    })
    this.webSocketService.getMessage("alarm_status").subscribe(data => {
      console.log(data)
      this.dmsLoadingData = data
      this.isAlarmActive = data["active"]
      if(this.isAlarmActive)
        this.activateBuzzers()
      else
        this.deactivateBuzzers()
    })
    this.webSocketService.getMessage("dms_key").subscribe(data => {
      this.dmsData = data["value"]
    })
    this.webSocketService.getMessage("rpir_data").subscribe(data => {
      this.rpirData = data
    })
    this.webSocketService.getMessage("gsg").subscribe(data => {
      this.handleGSGData(data)
    })
    this.webSocketService.getMessage("Humidity").subscribe(data => {
      this.humidity = data["value"]
    })
    this.webSocketService.getMessage("Temperature").subscribe(data => {
      this.temperature = data["value"]
    })

    this.webSocketService.getData()
  }

  handleGSGData(data : any){
    this.gsgData = data["gsg"]
      if(this.isAlarmActive == true)
        return
      this.isAlarmActive = true;
        console.log("upalio se alarm")
        data = {
          "last_activated_by" : "GSG",
          "activated_by" : "GSG"
        }
        this.openOrUpdateAlarmDialog(data);
  }

  deactivateBuzzers(){
    clearInterval(this.alarmInterval)
  }

  activateBuzzers(){
    let BBaudio = new Audio();
    let DBaudio = new Audio();
    BBaudio.src = "../../../assets/audio/alarmClock.WAV";
    BBaudio.load();
    DBaudio.src = "../../../assets/audio/alarm.mp3";
    DBaudio.load();
    this.alarmInterval = setInterval(() => {
      BBaudio.play();
      DBaudio.play()
    }, 3000)
  }

  handleData(data : any){
    // console.log(data);
      if (data.room === 'COVERED PORCH') {
        this.coveredPorchData = data;
      }else if(data.room==='LIGHT DATA'){
        this.lightData = data;
      }else if(data.room === 'GARAGE'){
        this.garageData = data;
      }else if(data.room==='COVERED PORCH-DS'){
        this.doorSensorCPdata = data;
      }else if(data.room==='GARAGE-DS'){
        this.doorSensorGdata = data;
      }else if(data.room==='ALARM'){
        if(data.state==true){
          this.isAlarmActive = true;
          console.log("upalio se alarm")
          this.openOrUpdateAlarmDialog(data);
        }else{
          console.log("ugasio se alarm")
          this.isAlarmActive = false;
          this.closeAlarmDialog();
        }
      }else if(data.room==="OWNER SUITE-B4SD"){
          console.log(this.timeData);
          this.timeData = data;
      }else if(data.room==="COVERED PORCH-BRGB"){
        this.colorData = data;
        console.log(this.colorData);
      }else if(data.room==="OWNER SUITE-BIR"){
        this.buttonPressedData = data;
        console.log(this.buttonPressedData);
    } 
    this.webSocketService.getData()
  }

  openOrUpdateAlarmDialog(data: any) {
    if (!this.alarmDialogRef || !this.alarmDialogRef.getState()) {
      this.alarmDialogRef = this.dialog.open(AlarmComponent, {
        width: '350px',
        data: data
      });
      this.alarmDialogRef.afterClosed().subscribe(() => {
        this.alarmDialogRef = null;
      });
    } else {
      this.alarmDataService.updateAlarmData(data);
    }
  }

  closeAlarmDialog() {
    if (this.alarmDialogRef) {
      this.alarmDialogRef.close();
      this.alarmDialogRef = null;
    }
  }
}
