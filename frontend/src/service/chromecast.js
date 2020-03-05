import gql from 'graphql-tag';
import client from './client';
import chromecastStore from '../store/chromecastStore';

const ALL = () => gql`
query {
 chromecastDeviceAll {
    name,
    uuid,
    isIdle,
    uri,
    host,
    port,
    mediaController {
      appId,
      isActive,
      isIdle,
      isPaused,
      isPlaying,
      mediaSessionId,
      status {
        title,
        contentId,
        contentType,
        currentTime,
        duration,
        lastUpdated,
        playbackRate,
        playerState,
        volumeLevel,
        volumeMuted 
      }
    }
  } 
}`;

const MEDIA_STATUS = () => gql`
subscription {
  mediaStatus {
    uuid,   
    contentId,
    contentType,
    currentTime,
    duration,
    lastUpdated,
    playbackRate,
    playerState,
    volumeLevel,
    volumeMuted   
  }
}
`;

export const chromecastMediaStatusSubscribe = () => {
  const s = client.subscribe({
    query: MEDIA_STATUS(),
  }).subscribe({
    next(data) {
      const ms = data.data.mediaStatus;
      chromecastStore.mediaStatus[ms.uuid] = ms;
      chromecastStore.refresh(ms.uuid);
    },
  });
  return s;
};

export const chromecastDeviceAll = (store) => client.query({
  query: ALL(),
  fetchPolicy: 'network-only',
}).then((resp) => {
  store.setState({
    chromecast: resp.data.chromecastDeviceAll,
  });
  store.refresh('chromecast');
  console.log('chromecastDeviceAll.setState', store.chromecast);
}).catch((error) => console.error(error));
