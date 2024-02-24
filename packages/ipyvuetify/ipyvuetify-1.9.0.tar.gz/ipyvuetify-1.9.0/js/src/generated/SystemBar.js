import { VuetifyWidgetModel } from './VuetifyWidget';

export class SystemBarModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'SystemBarModel',
                absolute: null,
                app: null,
                color: null,
                dark: null,
                fixed: null,
                height: undefined,
                light: null,
                lights_out: null,
                window: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-system-bar';
    }
}

SystemBarModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
