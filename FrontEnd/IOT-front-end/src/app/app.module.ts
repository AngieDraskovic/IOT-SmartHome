import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomePageComponent } from './components/home-page/home-page.component';
import { HeaderComponent } from './components/header/header.component';
import { FormsModule } from '@angular/forms';
import { SecurityComponent } from './components/security/security.component';
import { DLComponent } from './components/actuators/dl/dl.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {MatCardModule} from '@angular/material/card';
import { CoveredPorchComponent } from './components/rooms/covered-porch/covered-porch.component';
import { DpirComponent } from './components/sensors/dpir/dpir.component';
import { GarageComponent } from './components/rooms/garage/garage.component';
import { GlcdComponent } from './components/lcds/glcd/glcd.component';
import { OwnerSuiteComponent } from './components/rooms/owner-suite/owner-suite.component';
import { BrgbComponent } from './components/lcds/brgb/brgb.component';
import { HttpClientModule } from '@angular/common/http';
import { SocketIoConfig, SocketIoModule } from 'ngx-socket-io';


const config: SocketIoConfig = { url: 'http://localhost:5000', options: {} };


@NgModule({
  declarations: [
    AppComponent,
    HomePageComponent,
    HeaderComponent,
    SecurityComponent,
    DLComponent,
    CoveredPorchComponent,
    DpirComponent,
    GarageComponent,
    GlcdComponent,
    OwnerSuiteComponent,
    BrgbComponent,

  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    BrowserAnimationsModule,
    MatButtonModule,
    MatIconModule,
    MatCardModule,
    HttpClientModule,
    SocketIoModule.forRoot(config),

  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }

