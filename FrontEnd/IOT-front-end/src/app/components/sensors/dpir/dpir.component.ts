import { HttpClient } from '@angular/common/http';
import { Component, OnDestroy, OnInit } from '@angular/core';

import { Subscription } from 'rxjs';
import { ApiService } from 'src/app/api.service';
import { WebsocketService } from 'src/app/websocket.service';


@Component({
  selector: 'app-dpir',
  templateUrl: './dpir.component.html',
  styleUrls: ['./dpir.component.css']
})
export class DpirComponent implements OnInit, OnDestroy {
  motionHappened:boolean = false;
  peopleCount:number = 0;
  entryType:string = 'none';  // i nek se sa servera salje 'exit ili 'entry'
  private intervalId!: any;
  private updateSubscription!: Subscription;

  constructor(private apiService: ApiService, private http: HttpClient) {
  }

  ngOnInit() {
    this.intervalId = setInterval(() => {
      this.http.get('http://localhost:5000/get-latest-mqtt-message').subscribe(
        (data) => {
          console.log(data);
          // Obrada primljenih podataka
        },
        (error) => {
          console.error('Error:', error);
        }
      );
    }, 1000); // 1000 ms = 1 sekunda
  }

  read() {
    this.updateSubscription = this.apiService.toggleLight().subscribe(
      (data: any) => {
        console.log(data);
        // // Obrada podataka
        // // Pretpostavimo da 'data' sadrži polje 'entryType'
        // this.entryType = data.entryType;
        // this.motionHappened = data.entryType === 'entry';
      },
      (error) => {
        console.error('Error fetching data:', error);
      }
    );
  }

  ngOnDestroy(): void {
    if (this.updateSubscription) {
      this.updateSubscription.unsubscribe();
    }
  }
}
