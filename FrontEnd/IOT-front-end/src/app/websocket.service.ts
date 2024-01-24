import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { io, Socket } from 'socket.io-client';

@Injectable({
  providedIn: 'root'
})
export class WebsocketService {
  private socket: Socket;

  constructor() {
    this.socket = io('http://localhost:5000'); // URL vašeg Flask servera
    console.log("WebsocketService: Socket initialized."); // Logujete inicijalizaciju socket-a
  }

  listen(eventName: string): Observable<any> {
    console.log(`WebsocketService: Listening for event: ${eventName}`); // Logujete početak osluškivanja događaja
    return new Observable((subscriber) => {
      this.socket.on(eventName, (data) => {
        console.log(`WebsocketService: Received data for event ${eventName}:`, data); // Logujete primljene podatke
        subscriber.next(data);
      });
    });
  }
}
