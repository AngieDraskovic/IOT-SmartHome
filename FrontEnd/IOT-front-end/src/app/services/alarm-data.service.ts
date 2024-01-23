import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AlarmDataService {
  private alarmDataSubject = new BehaviorSubject<any>(null);
  public alarmData$ = this.alarmDataSubject.asObservable();

  updateAlarmData(data: any) {
    this.alarmDataSubject.next(data);
  }
}
