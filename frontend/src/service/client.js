import { ApolloClient } from 'apollo-client';
import { ApolloLink } from 'apollo-link';
import { HttpLink } from 'apollo-link-http';
import { WebSocketLink } from 'apollo-link-ws';
import { getMainDefinition } from 'apollo-utilities';
import { InMemoryCache } from 'apollo-cache-inmemory';

const httpUri = `http://${window.playlistcast.uri}/graphql`;
const wsUri = `ws://${window.playlistcast.uri}/subscriptions`;

const link = ApolloLink.split(
  ({ query }) => {
    console.log('!@.service.client', query);
    const definition = getMainDefinition(query);
    return (
      definition.kind === 'OperationDefinition'
      && definition.operation === 'subscription'
    );
  },
  new WebSocketLink({
    uri: wsUri,
    options: {
      reconnect: true,
      connectionParams: {
        authToken: '',
      },
    },
  }),
  new HttpLink({ uri: httpUri }),
);

// eslint-disable-next-line no-underscore-dangle
const cache = new InMemoryCache(window.__APOLLO_STATE);
const client = new ApolloClient({
  link,
  cache,
});

export default client;
