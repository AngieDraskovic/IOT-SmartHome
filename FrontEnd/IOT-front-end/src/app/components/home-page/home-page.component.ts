import { Component, OnInit } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { WebSocketService } from 'src/app/services/web-socket.service';

@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.css']
})
export class HomePageComponent implements OnInit{
  constructor(private webSocketService : WebSocketService, private socket : Socket) {
  }
  coveredPorchData: any;
  lightData:any;        // ide i on za coveredPorch ali je drugaciji child pa sam ovako

  garageData:any;
  ngOnInit(): void {
    this.webSocketService.getMessage().subscribe(data => {
      console.log(data);
      if (data.room === 'COVERED PORCH') {
        this.coveredPorchData = data;
      }else if(data.room==='LIGHT DATA'){
        this.lightData = data;
      }else if(data.room === 'GARAGE'){
        this.garageData = data;
      }
    })

    this.webSocketService.getData()
  }

}
