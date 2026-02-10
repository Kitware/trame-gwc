import GWC from '@girder/components';
import '@girder/components/style.css';
import GirderProvider from './components/restProvider.vue';

export default function install(app, options) {
    app.use(GWC, options);
    app.component('GirderProvider', GirderProvider);
}