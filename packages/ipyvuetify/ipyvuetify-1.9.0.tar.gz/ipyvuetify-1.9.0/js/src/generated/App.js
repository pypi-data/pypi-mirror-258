import { VuetifyWidgetModel } from './VuetifyWidget';

export class AppModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'AppModel',
                dark: null,
                id: null,
                light: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-app';
    }
}

AppModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
