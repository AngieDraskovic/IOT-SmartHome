import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient) { }

  toggleLight() {

    return this.http.get('http://localhost:5000/test_emit');
  }
}
