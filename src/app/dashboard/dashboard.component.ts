import { Component, OnInit } from '@angular/core';
import { ElectronService } from 'ngx-electron';
import { RestService } from '../rest.service';
import { ActivatedRoute, Router } from '@angular/router';
import { ButtonsModule } from 'ngx-bootstrap/buttons';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {

  folder: string[];
  status: string[];
  loadingMessage: any;
  errorMessage: any;
  noUiSlider: any;

  constructor(private _electronService: ElectronService, public rest:RestService, private route: ActivatedRoute, private router: Router) { }

  ngOnInit() {
    this.getDummyData();


  }

  getServerStatus() {
    this.rest.getServerStatus().subscribe((data) => {
      console.log(data);
      this.status = data;
    });
  }

  getDummyData() {
    this.loadingMessage = true;

    this.rest.getDummyData().subscribe((data) => {
      console.log(data);
      this.loadingMessage = false;
    },
    (err: any) => {
      this.errorMessage = "There are no posts pulled from the server!";
      this.loadingMessage = false;
    });
  }

  openDialog(){
    console.log("function called");
    this._electronService.remote.dialog.showOpenDialog({title: 'Select a folder', properties: ['openFile']}, (db_file) => {
      if (db_file === undefined){
          console.log("You didn't select a folder");
          return;
      } else {
        console.log(db_file[0])
        console.log(db_file);
      }      
    });
  }

}
