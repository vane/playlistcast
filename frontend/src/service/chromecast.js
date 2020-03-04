import gql from 'graphql-tag';
import client from './client';

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
        contentType,
        volumeLevel,
        volumeMuted
      }
    }
  } 
}`;

const chromecastDeviceAll = (store) => client.query({
  query: ALL(),
  fetchPolicy: 'network-only',
}).then((resp) => {
  store.setState({
    chromecast: resp.data.chromecastDeviceAll,
  });
  store.refresh('chromecast');
  console.log('chromecastDeviceAll.setState', store.chromecast);
}).catch((error) => console.error(error));

export default chromecastDeviceAll;
