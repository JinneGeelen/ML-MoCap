import { Component } from '@angular/core';
import { ThemeService } from 'app/core/service/theme.service';

@Component({
  selector: 'app-nav',
  templateUrl: './nav.component.html',
  styleUrls: ['./nav.component.scss']
})
export class NavComponent {
  navItems = [
    { link: '/studies', title: 'Studies' },
    { link: '/participants', title: 'Participants' },
    { link: '/recordings', title: 'Recordings' },
    { link: '/cameras', title: 'Cameras' },
    { link: '/diagnostics', title: 'Diagnostics' },
  ];

  constructor(
    private themeService: ThemeService
  ) {}

  public toggleDarkTheme() {
    this.themeService.toggleDarkTheme();
  }

  get isDarkTheme() {
    return this.themeService.isDarkTheme;
  }
}
