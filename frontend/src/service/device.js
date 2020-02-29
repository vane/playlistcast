import gql from 'graphql-tag';
import client from './client';

const GET = () => gql`
query {
 allChromecastDevice {
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
        contentType
      }
    }
  } 
}`;

const chromecastDeviceAll = (store) => client.query({
  query: GET(),
  fetchPolicy: 'network-only',
}).then((resp) => {
  store.setState({
    chromecast: resp.data.allChromecastDevice,
  });
  store.refresh('chromecast');
  console.log('chromecastDeviceAll.setState', store.chromecast);
}).catch((error) => console.error(error));

export default chromecastDeviceAll;
