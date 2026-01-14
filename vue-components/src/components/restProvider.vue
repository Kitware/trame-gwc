<template>
  <div>
    <slot></slot>
  </div>
</template>

<script>
  import { provide } from 'vue';
  import { useGirderClient, useNotificationBus } from '@girder/components';

  export default {
    name: 'GirderProvider',
    emits: ['login', 'logout', 'register', 'setApiRoot', 'fetchUser'],
    props: {
      computeNotificationBus: {type: Boolean, default: false},
      listenToRestClient: {type: Boolean, default: true},
      useEventSource: {type: Boolean, default: false},
      withCredentials: {type: Boolean, default: true},
      apiRoot: {type: String, default: null},
      authenticateWithCredentials: {type: Boolean, default: false},
      useGirderAuthorizationHeader: {type: Boolean, default: false},
      setLocalCookie: {type: Boolean, default: true},
    },
    setup(props, ctx) {
      const girder = useGirderClient(
        {
          apiRoot: props.apiRoot,
          authenticateWithCredentials: props.authenticateWithCredentials,
          useGirderAuthorizationHeader: props.useGirderAuthorizationHeader,
          setLocalCookie: props.setLocalCookie,
        }
      );

      if (girder.apiRoot.value) {
        fetchUser();
      }
      provide('girder', girder);

      if (props.computeNotificationBus) {
        const notification = useNotificationBus(
          girder.rest,
          {
            useEventSource: props.useEventSource,
            withCredentials: props.withCredentials,
            listenToRestClient: props.listenToRestClient
          }
        );
        if (girder.user.value) {
          notification.connect();
        }
        provide('notification', notification);
      }
      
      girder.rest.on('userLoggedIn', () => {ctx.emit('userLoggedIn', { user: girder.user.value, token: girder.token.value })});

      girder.rest.on('userLoggedOut', () => {ctx.emit('userLoggedOut')});

      girder.rest.on('apiRootUpdated', () => {ctx.emit('apiRootUpdated', { apiRoot: girder.apiRoot.value, user: girder.user.value, token: girder.token.value })});

      girder.rest.on('userRegistered', () => {ctx.emit('userRegistered', { user: girder.user.value, token: girder.token.value })});

      girder.rest.on('userFetched', () => {ctx.emit('userFetched', { user: girder.user.value, token: girder.token.value })});
    
      function logout() {
        girder.rest.logout();
      }

      function login(username, password, otp = null) {
        girder.rest.login(username, password, otp);
      }

      function register(login, email, firstName, lastName, password, admin = false) {
        girder.rest.register(login, email, firstName, lastName, password, admin);
      }

      async function setApiRoot(apiRoot) {
        await girder.rest.setApiRoot(apiRoot);
      }

      async function fetchUser() {
        await girder.rest.fetchUser()
      }

      return {
        fetchUser,
        login,
        logout,
        register,
        setApiRoot
      }
    },
  }
</script>
