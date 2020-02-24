import gql from 'graphql-tag';
import client from './client';

const GET = () => gql`
query {
 allResourceLocation {
    id,
    name,
    location,
    protocol
  } 
}`;

const DELETE = (name) => gql`
mutation {
  delResourceLocation(name:"${name}") {
    name
  }
}
`;

const POST = () => gql`
mutation post($data: ResourceLocationInput!) {
  postResourceLocation(data:$data) {
    id,
    name,
    location,
    protocol
  }
}
`;

const PUT = () => gql`
mutation put($data: ResourceLocation!, $id:ID!) {
  putResourceLocation(data:$data, id:$id) {
    id,
    name
  }
}
`;


export const resourceLocationAll = (store) => client.query({
  query: GET(),
  fetchPolicy: 'network-only',
}).then((resp) => {
  store.setState({
    location: resp.data.allResourceLocation,
  });
  store.refresh();
  console.log('resourceLocationAll.setState', store.allResourceLocation);
}).catch((error) => console.error(error));

export const resourceLocationDel = (store, name) => client.mutate({
  mutation: DELETE(name),
}).then(() => {
  resourceLocationAll(store);
}).catch((error) => console.error(error));

export const resourceLocationAdd = (store, data) => client.mutate({
  variables: { data },
  mutation: POST(),
}).then(() => {
  resourceLocationAll(store);
}).catch((error) => console.error(error));

export const resourceLocationEdit = (store, data, id) => client.mutate({
  variables: {
    ...data,
    id,
  },
  mutation: PUT(),
}).then(() => {
  resourceLocationAll(store);
}).catch((error) => console.error(error));
