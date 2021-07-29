import { Component } from '@angular/core';
import { ThemeService } from '@core/service/theme.service';

@Component({
  selector: 'app-content-layout',
  templateUrl: './content-layout.component.html',
  styleUrls: ['./content-layout.component.scss']
})
export class ContentLayoutComponent {
  constructor(
    private themeService: ThemeService
  ) {}

  get theme() {
    return this.themeService.isDarkTheme ? 'my-dark-theme' : 'my-light-theme';
  }
}
