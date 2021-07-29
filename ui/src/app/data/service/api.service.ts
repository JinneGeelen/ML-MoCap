import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { filter, map } from 'rxjs/operators';
import { environment } from '../../../environments/environment';

interface Entity {
  id?: string;
}

interface EntityMessage {
  event: string;
  entity: any;
}

@Injectable({
  providedIn: 'root'
})
export class APIService<T extends Entity> {
  protected resource: string = null;
  protected sortProperty: string[] = ['id'];

  protected _socket: WebSocket;

  protected _entities$ = new BehaviorSubject<T[]>([]);
  protected _entity$ = new BehaviorSubject<T>(null);
  protected _entities: { [id: string]: T };


  constructor(protected http: HttpClient) { }

  protected get resourceUrl(): string {
    return `http://${environment.serverUrl}/${this.resource}/`;
  }

  protected get resourceSocketUrl(): string {
    return `ws://${environment.serverUrl}/${this.resource}/ws`;
  }

  protected sortFn(a: T, b: T): number {
    for (let i = 0; i < this.sortProperty.length; i++) {
      const sortProperty = this.sortProperty[i];
      if (a[sortProperty] > b[sortProperty]) {
        return 1;
      } else if (a[sortProperty] < b[sortProperty]) {
        return -1;
      }
    }
    return 0
  }

  public async list(): Promise<T[]> {
    return await <Promise<T[]>>this.http.get(this.resourceUrl).toPromise();
  }

  public async create(entity: T): Promise<T> {
    return await <Promise<T>>this.http.post(this.resourceUrl, entity).toPromise();
  }

  public async read(id: string): Promise<T> {
    return await <Promise<T>>this.http.get(`${this.resourceUrl}${id}`).toPromise();
  }

  public async update(entity: T): Promise<T> {
    return await <Promise<T>>(this.http.put(`${this.resourceUrl}${entity.id}`, entity)).toPromise();
  }

  public async delete(id: string): Promise<T> {
    return await <Promise<T>>this.http.delete(`${this.resourceUrl}${id}`).toPromise();
  }

  public watchAll(): Observable<T[]> {
    if (!this._socket) {
      this.connect();
    }

    return this._entities$.asObservable().pipe(
      map(value => value.sort(this.sortFn.bind(this)))
    );
  }

  public watch(id: string): Observable<T> {
    return this._entity$.asObservable().pipe(
      filter(entity => {
        return entity.id == id;
      })
    );
  }

  protected parseEntity(record: T): T {
    return record;
  }

  protected async connect() {
    const entities = await this.list();

    this._entities$.next(entities);

    this._entities = {};
    entities.forEach(entity => {
      this._entities[entity.id] = entity;
      this._entity$.next(entity);
    });

    this._socket = new WebSocket(this.resourceSocketUrl);

    this._socket.onmessage = (event: MessageEvent) => {
      const message: EntityMessage = JSON.parse(event.data);
      const entity: T = this.parseEntity(message.entity);

      switch (message.event) {
        case 'delete':
          delete this._entities[entity.id];
          this._entities$.next(Object.values(this._entities));
          break;

        case 'create':
        case 'update':
          this._entities[entity.id] = entity;
          this._entities$.next(Object.values(this._entities));
          this._entity$.next(entity);
          break;
      }
    };

    this._socket.onerror = this._entities$.error.bind(this._entities$);
    this._socket.onclose = () => {
      this._entities$.complete.bind(this._entities$);
      this._socket = null;
    };
  }
}
