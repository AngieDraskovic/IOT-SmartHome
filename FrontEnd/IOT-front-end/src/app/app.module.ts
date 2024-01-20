import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomePageComponent } from './components/home-page/home-page.component';
import { HeaderComponent } from './components/header/header.component';
import { SecurityComponent } from './components/security/security.component';
import { FormsModule } from '@angular/forms';
import { IMqttServiceOptions, MqttModule } from 'ngx-mqtt';
import { DLComponent } from './components/actuators/dl/dl.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {MatCardModule} from '@angular/material/card';
import { CoveredPorchComponent } from './components/rooms/covered-porch/covered-porch.component';
import { DpirComponent } from './components/sensors/dpir/dpir.component';

export const MQTT_SERVICE_OPTIONS: IMqttServiceOptions = {
  hostname: 'localhost', // Change this to your MQTT broker hostname
  port: 9001, // Change this to your MQTT broker port
  path: '/mqtt' // Change this to your MQTT broker path (if applicable)
};


@NgModule({
  declarations: [
    AppComponent,
    HomePageComponent,
    HeaderComponent,
    SecurityComponent,
    DLComponent,
    CoveredPorchComponent,
    DpirComponent,
   
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    MqttModule.forRoot(MQTT_SERVICE_OPTIONS),
    BrowserAnimationsModule,
    MatButtonModule,
    MatIconModule,
    MatCardModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }

