import gql from 'graphql-tag';
import client from './client';

const GET = () => gql`
query {
 firstStart {
    value
  } 
}`;

const POST = () => gql`
mutation post($data: FirstStartInput!) {
  postFirstStart(data:$data) {
    value
  }
}
`;

export const firstStartGet = (store) => client.query({
  query: GET(),
  fetchPolicy: 'network-only',
}).then((resp) => {
  store.setState(resp.data.firstStart);
  store.refresh();
  console.log('getFirstStart.setState', store.value);
}).catch((error) => console.error(error));

export const firstStartAdd = (store, data) => client.mutate({
  variables: { data },
  mutation: POST(),
}).then(() => {
  firstStartGet(store);
}).catch((error) => console.error(error));
