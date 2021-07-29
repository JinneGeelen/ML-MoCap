export interface Camera {
  id: string;
  position: string;
  connected: boolean;
  settings: CameraSettings;
  state?: string;
  order?: number;
}

export interface CameraSettings {
  id: string;
  width: number;
  height: number;
  fps: number;
}

export interface Diagnostic {
  id?: string;
  iterations: number;
  start_time?: Date;
  end_time?: Date;
  is_running?: boolean;
}

export interface DiagnosticResult {
  id: string;
  diagnostic_id: string;
  camera_id: string;
  iteration: number;
  time_start_requested: Date;
  time_socket_received: Date;
  time_preview_started: Date;
  time_recording_start: Date;
  time_recording_started: Date;
  time_recording_stop: Date;
  time_recording_stopped: Date;
  delta_sync: number;
  delta_recording: number;
  delta_start_recording: number;
  delta_stop_recording: number;
}

export interface Study {
  id?: string;
  name: string;
  researcher: string;
  date: string;
  emg: boolean;
}

export interface Participant {
  id?: string;
  study_id: string;
  study?: Study;
  number: string;
  age: number;
  gender: string;
  dominant_hand: string;
  consent_video: boolean;
}

export interface Recording {
  id?: string;
  participant_id: string;
  participant?: Participant;
  name: string;
  filepath: string;
  start_time: string;
  end_time: string;
  state: string;
  cameras_recorded: string;
  cameras_processing: string;
  cameras_processed: string;
}
