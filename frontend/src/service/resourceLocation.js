import gql from 'graphql-tag';
import client from 'service/client';

const ALL = () => gql`
query {
 resourceLocationAll {
    id,
    name,
    location,
    protocol
  } 
}`;

const DELETE = (id) => gql`
mutation {
  resourceLocationDelete(id:"${id}") {
    id
  }
}
`;

const ADD = () => gql`
mutation post($data: ResourceLocationInput!) {
  resourceLocationAdd(data:$data) {
    id,
    name,
    location,
    protocol
  }
}
`;

const CHANGE = () => gql`
mutation put($data: ResourceLocationInput!, $id:ID!) {
  putResourceLocationChange(data:$data, id:$id) {
    id,
    name,
    location,
    protocol 
  }
}
`;

const LIST_DIR = (name, subpath) => gql`
query {
  listDirectory(name:${name}, subpath:${subpath})
}
`;


export const resourceLocationAll = (store) => client.query({
  query: ALL(),
  fetchPolicy: 'network-only',
}).then((resp) => {
  store.setState({
    location: resp.data.resourceLocationAll,
  });
  store.refresh();
  console.log('resourceLocationAll.setState', store.resourceLocationAll);
}).catch((error) => console.error(error));

export const resourceLocationDel = (store, id) => client.mutate({
  mutation: DELETE(id),
}).then(() => {
  resourceLocationAll(store);
}).catch((error) => console.error(error));

export const resourceLocationAdd = (store, data) => client.mutate({
  variables: { data },
  mutation: ADD(),
}).then(() => {
  resourceLocationAll(store);
}).catch((error) => console.error(error));

export const resourceLocationChange = (store, data, id) => client.mutate({
  variables: {
    data,
    id,
  },
  mutation: CHANGE(),
}).then(() => {
  resourceLocationAll(store);
}).catch((error) => console.error(error));

export const listDirectory = (store, name, subpath) => client.query({
  query: LIST_DIR(name, subpath),
  fetchPolicy: 'network-only',
}).then((resp) => {
  console.log(resp.data);
  store.refresh();
}).catch((error) => console.error(error));
