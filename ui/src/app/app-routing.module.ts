import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ContentLayoutComponent } from '@layout/content-layout/content-layout.component';

const routes: Routes = [
  {
    path: '',
    redirectTo: '/studies/list',
    pathMatch: 'full'
  },
  {
    path: '',
    component: ContentLayoutComponent,
    children: [
      {
        path: 'studies',
        loadChildren: () =>
          import('@modules/studies/studies.module').then(m => m.StudiesModule)
      },
      {
        path: 'participants',
        loadChildren: () =>
          import('@modules/participants/participants.module').then(m => m.ParticipantsModule)
      },
      {
        path: 'recordings',
        loadChildren: () =>
          import('@modules/recordings/recordings.module').then(m => m.RecordingsModule)
      },
      {
        path: 'cameras',
        loadChildren: () =>
          import('@modules/cameras/cameras.module').then(m => m.CamerasModule)
      },
      {
        path: 'diagnostics',
        loadChildren: () =>
          import('@modules/diagnostics/diagnostics.module').then(m => m.DiagnosticsModule)
      },
    ]
  },
  // Fallback when no prior routes is matched
  { path: '**', redirectTo: '/studies/list', pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { useHash: true, relativeLinkResolution: 'legacy' })],
  exports: [RouterModule],
  providers: []
})
export class AppRoutingModule {}
