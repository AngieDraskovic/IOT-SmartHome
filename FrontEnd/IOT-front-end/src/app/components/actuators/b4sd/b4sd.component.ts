import { Component, Input, SimpleChanges } from '@angular/core';

@Component({
  selector: 'app-b4sd',
  templateUrl: './b4sd.component.html',
  styleUrls: ['./b4sd.component.css']
})
export class B4sdComponent {
  @Input() time:string ="08:00";
  @Input() isAlarmActive : boolean = false;
  opacity = true;
  intervalId : any;

  ngOnChanges(changes: SimpleChanges): void {
    console.log(changes)
    if(changes['isAlarmActive'] && changes['isAlarmActive'].currentValue != changes['isAlarmActive'].previousValue){
      this.setBlinking(changes['isAlarmActive'].currentValue)
    }
  }

  setBlinking(active : any){
    if(active == true){
      this.intervalId = setInterval(() => {
          this.opacity = !this.opacity
        }, 500)
    }
    else{
      clearInterval(this.intervalId)
      this.opacity = true
    }
  }
}
