import ReactDOM from 'react-dom';
import React from 'react';
import timeSubscribe from './service/time';
import PlaylistCast from './view/playlistcast';

timeSubscribe();
ReactDOM.render(<PlaylistCast />, document.getElementById('app'));
