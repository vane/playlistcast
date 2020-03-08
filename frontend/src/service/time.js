import gql from 'graphql-tag';
import client from 'service/client';
import timeStore from 'store/timeStore';


const SUBSCRIBE = () => gql`
subscription {
  time {
    id,
    time
  }
}`;

const timeSubscribe = () => {
  const s = client.subscribe({
    query: SUBSCRIBE(),
  }).subscribe({
    next(data) {
      timeStore.setState({ time: Date.parse(data.data.time.time) });
      timeStore.refresh('updateTime');
    },
  });
  return s;
};

export default timeSubscribe;
