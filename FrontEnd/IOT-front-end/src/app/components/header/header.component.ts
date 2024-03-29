import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent {
  constructor(private router : Router){

  }

  goToSecurityPage(){
    this.router.navigate(["security"])
  }

  goToGrafanaPage(){
    this.router.navigate(["grafana"])
  }

  
  goToHomePage(){
    this.router.navigate([""])
  }

}
