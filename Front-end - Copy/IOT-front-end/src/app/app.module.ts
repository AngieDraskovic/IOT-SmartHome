import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomePageComponent } from './components/home-page/home-page.component';
import { HeaderComponent } from './components/header/header.component';
import { SecurityComponent } from './components/security/security.component';
import { FormsModule } from '@angular/forms';
import { IMqttServiceOptions, MqttModule } from 'ngx-mqtt';

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
    SecurityComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    MqttModule.forRoot(MQTT_SERVICE_OPTIONS),
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }

