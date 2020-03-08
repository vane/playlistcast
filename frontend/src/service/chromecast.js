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
    status {
      volumeLevel,
      volumeMuted
    },
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
        playerState
      }
    }
  } 
}`;

const PAUSE = (uid) => gql`
mutation {
  chromecastPause(uid:"${uid}")
}
`;

const PLAY = (uid) => gql`
mutation {
  chromecastPlay(uid:"${uid}")
}
`;

const VOLUME_CHANGE = (uid, volume) => gql`
mutation {
  chromecastVolumeChange(uid:"${uid}", volume:${volume})
}
`;

const SEEK = (uid, value) => gql`
mutation {
  chromecastSeek(uid:"${uid}", value:${value})
}
`;

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

export const chromecastPause = (uid) => client.mutate({
  mutation: PAUSE(uid),
});

export const chromecastPlay = (uid) => client.mutate({
  mutation: PLAY(uid),
});

export const chromecastVolumeChange = (uid, volume) => client.mutate({
  mutation: VOLUME_CHANGE(uid, volume),
});

export const chromecastSeek = (uid, value) => client.mutate({
  mutation: SEEK(uid, value),
});
