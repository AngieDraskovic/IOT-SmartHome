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
export class DpirComponent {
  @Input() motionHappened: boolean = false;
  @Input() peopleCount: number = 0;
  @Input() entryType: string = 'none';
  @Input() data: any;
  @Input() id:string = "";

 

}
