import ReactDOM from 'react-dom';
import React from 'react';
import timeSubscribe from 'service/time';
import PlaylistCast from 'view/playlistcast';
import { chromecastMediaStatusSubscribe } from 'service/chromecast';

timeSubscribe();
chromecastMediaStatusSubscribe();
ReactDOM.render(<PlaylistCast />, document.getElementById('app'));
