import { Injectable } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})


export class WebSocketService {
  
  constructor(private socket: Socket) {
    this.socket.on('connect', () => {
      console.log('WebSocket connected');
    });
    this.socket.on('disconnect', () => {
      console.log('WebSocket disconnected');
    });
  }

  getData(){
    setInterval(() => {
      this.socket.emit('get_data', {"message" : "Retrieve PI data"});
    }, 1000)
  }

  sendMessage(topic : string, message: any) {
    this.socket.emit(topic, {"message" : message});
  }

  getMessage(topic = 'front_data') {
    return this.socket.fromEvent(topic).pipe(map((data: any) => data))
  }

}
