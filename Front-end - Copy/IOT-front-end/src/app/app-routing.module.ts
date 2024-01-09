import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomePageComponent } from './components/home-page/home-page.component';
import { SecurityComponent } from './components/security/security.component';

const routes: Routes = [
  { path : '', component: HomePageComponent},
  { path: 'security', component: SecurityComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
