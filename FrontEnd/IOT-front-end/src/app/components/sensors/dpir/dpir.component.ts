import { Component, OnDestroy, OnInit } from '@angular/core';

import { Subscription } from 'rxjs';
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
  private updateSubscription!: Subscription;

  constructor(private websocketService: WebsocketService) {
  }

  ngOnInit(): void {
    this.updateSubscription = this.websocketService.listen('update_data').subscribe((data) => {
     
      console.log(data);
      // Obradite primljene podatke
    });
  }

  ngOnDestroy(): void {
    if (this.updateSubscription) {
      this.updateSubscription.unsubscribe();
    }
  }
}
