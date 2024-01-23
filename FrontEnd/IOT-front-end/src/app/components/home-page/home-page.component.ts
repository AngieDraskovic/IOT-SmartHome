import { Component, OnInit } from '@angular/core';
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
  isAlarmActive = false;
  alarmDialogRef: any; 

  ngOnInit(): void {
    this.webSocketService.getMessage().subscribe(data => {
      this.handleData(data)
    })
    this.webSocketService.getMessage("alarm_status").subscribe(data => {
      this.dmsLoadingData = data["active"]
    })
    this.webSocketService.getMessage("dms_key").subscribe(data => {
      this.dmsData = data["value"]
    })

    this.webSocketService.getData()
  }

  handleData(data : any){
    console.log(data);
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
          console.log("cao angie, UPALIOOOOOOO SE")
          this.openOrUpdateAlarmDialog(data);
        }else{
          console.log("cao ANGIEE UGASIOOO SE")
          this.isAlarmActive = false;
          this.closeAlarmDialog();
        }
      }
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
