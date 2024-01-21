import { Injectable } from '@angular/core';
import { Client } from '@stomp/stompjs';

@Injectable({
  providedIn: 'root'
})
export class WebSocketService {

  private stompClient:Client;
  constructor() {
    const stompConfig = {
      brokerURL: 'ws://localhost:9001', 
    }
    this.stompClient = new Client(stompConfig)
    this.stompClient.activate();
  }
  
  subscribe(destination: string, callback: any) {

    if(this.stompClient.connected){
      this.stompClient.subscribe(destination, callback);
    }else{
      this.stompClient.onConnect = (frame) => {
        this.stompClient.subscribe(destination, callback);
      }
    }
  }

  // Send a message to a WebSocket destination
  sendMessage(destination: string, body: string) {
    this.stompClient.publish({
      destination,
      body,
    });
  }
}
