import { HttpClient } from '@angular/common/http';
import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { Socket } from 'ngx-socket-io';

import { Subscription } from 'rxjs';
import { ApiService } from 'src/app/api.service';
import { WebSocketService } from 'src/app/services/web-socket.service';


@Component({
  selector: 'app-dpir',
  templateUrl: './dpir.component.html',
  styleUrls: ['./dpir.component.css']
})
export class DpirComponent implements OnChanges {
  motionHappened: boolean = false;
  peopleCount: number = 0;
  entryType: string = 'none';
  @Input() data: any;

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.data && this.data) {
      this.motionHappened = this.data.motion;
      this.peopleCount = this.data.people_count;
      this.entryType = this.data.action;
    }
  }

}
