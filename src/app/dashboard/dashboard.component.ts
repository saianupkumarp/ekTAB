import { Component, OnInit } from '@angular/core';
import { ElectronService } from 'ngx-electron';
import { RestService } from '../rest.service';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {

  folder: string[];
  status: string[];

  constructor(private _electronService: ElectronService, public rest:RestService, private route: ActivatedRoute, private router: Router) { }

  ngOnInit() {
    this.getServerStatus();
  }

  getServerStatus() {
    this.rest.getServerStatus().subscribe((data) => {
      console.log(data);
      this.status = data;
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
        console.log(db_file)
      }      
    });
  }

}
