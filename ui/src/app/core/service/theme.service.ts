import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ThemeService {
  private _isDarkTheme = true;

  get isDarkTheme() {
    return this._isDarkTheme;
  }

  public setDarkTheme(isDark: boolean) {
    this._isDarkTheme = isDark;
  }

  public toggleDarkTheme() {
    this.setDarkTheme(!this.isDarkTheme);
  }
}
