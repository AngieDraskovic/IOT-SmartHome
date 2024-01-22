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

  sendMessage(message: string) {
    this.socket.emit('test_message', {"message" : message});
  }

  getMessage() {
    return this.socket.fromEvent('data_testing').pipe(map((data: any) => data))
  }

}
