import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { NgxElectronModule } from 'ngx-electron';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { NvD3Module } from 'ngx-nvd3';

import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing-module';
import { DashboardComponent } from './dashboard/dashboard.component';
import { LineChartComponent } from './charts/line-chart/line-chart.component';
import { BarChartComponent } from './charts/bar-chart/bar-chart.component';
import { SidebarComponent } from './sidebar/sidebar.component';
import { HomeComponent } from './home/home.component';
import { LoaderComponent } from './loader/loader.component';

import { LoaderInterceptorService } from './loader-interceptor.service';

@NgModule({
  declarations: [
    AppComponent,
    DashboardComponent,
    LineChartComponent,
    BarChartComponent,
    SidebarComponent,
    HomeComponent,
    LoaderComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgxElectronModule,
    HttpClientModule,
    NvD3Module
  ],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: LoaderInterceptorService,
      multi: true
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
