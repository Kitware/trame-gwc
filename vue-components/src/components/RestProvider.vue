<template>
  <div>
    <slot></slot>
  </div>
</template>

<script>
import { RestClient, NotificationBus } from '@girder/components/src';
import { computed } from 'vue';
import { vuetifyConfig } from '@girder/components/src/utils';

export default {
  inject: ['trame'],
  data() {
    return {
      girderRest: null,
      notificationBus: null,
    };
  },
  async created() {
    // Register Girder Web Component icons mapping in Vuetify
    Object.assign(this.$vuetify.icons.values, vuetifyConfig.icons.values);

    this.girderRest = new RestClient({ apiRoot: this.trame.state.get('api_root') });
    this.notificationBus = new NotificationBus(this.girderRest, { useEventSource: true });

    const user = await this.girderRest.fetchUser();
    if (user) {
      this.trame.state.set('user', user);
      this.trame.state.set('token', this.girderRest.token);
      this.notificationBus.connect();
    }

    this.girderRest.$on('login', () => {
      this.login();
    });
  },
  provide() {
    return {
      girderRest: computed(() => this.girderRest),
      notificationBus: computed(() => this.notificationBus),
    };
  },
  methods: {
    async login() {
      const user = await this.girderRest.fetchUser();
      if (user) {
        this.trame.state.set('user', user);
        this.trame.state.set('token', this.girderRest.token);
      }
    },
    logout() {
      this.girderRest.logout();
      this.trame.state.set('user', null);
      this.trame.state.set('token', null);
    },
  },
};
</script>
