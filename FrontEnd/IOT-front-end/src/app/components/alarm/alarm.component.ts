import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialog } from '@angular/material/dialog';
import { AlarmDataService } from 'src/app/services/alarm-data.service';

@Component({
  selector: 'app-alarm',
  templateUrl: './alarm.component.html',
  styleUrls: ['./alarm.component.css']
})
export class AlarmComponent {

  
  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private alarmDataService: AlarmDataService
  ) {
    this.alarmDataService.alarmData$.subscribe(updatedData => {
      if (updatedData) {
        this.data = updatedData;
      }
    });
  }
}
