import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';

@Component({
  selector: 'app-rpir',
  templateUrl: './rpir.component.html',
  styleUrls: ['./rpir.component.css']
})
export class RpirComponent implements OnChanges{
  @Input() data : any;
  motionDetectedArr = [false, false, false, false]

  ngOnChanges(changes: SimpleChanges): void {
    console.log(changes)
    if(changes['data']){
      this.parseRpirData(changes['data'].currentValue)
    }
  }

  parseRpirData(data : any){
    console.log("test")
    let index = data["id"] - 1
    let value = data["value"]
    this.motionDetectedArr[index] = value
  }

  getTextByMotion(index : number) : string{
    if(this.motionDetectedArr[index] == false)
      return "No motion detected";
    else
      return "Motion detected"
  }
}
