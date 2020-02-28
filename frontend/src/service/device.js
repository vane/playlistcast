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
    port
  } 
}`;

const chromecastDeviceAll = (store) => client.query({
  query: GET(),
  fetchPolicy: 'network-only',
}).then((resp) => {
  store.setState({
    chromecast: resp.data.allChromecastDevice,
  });
  store.refresh();
  console.log('chromecastDeviceAll.setState', store.chromecast);
}).catch((error) => console.error(error));

export default chromecastDeviceAll;
