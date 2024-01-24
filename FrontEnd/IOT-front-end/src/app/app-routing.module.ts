import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomePageComponent } from './components/home-page/home-page.component';
import { SecurityComponent } from './components/security/security.component';
import { GrafanaPageComponent } from './components/grafana-page/grafana-page.component';

const routes: Routes = [
  { path : '', component: HomePageComponent},
  { path: 'security', component: SecurityComponent},
  { path: 'grafana', component: GrafanaPageComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
