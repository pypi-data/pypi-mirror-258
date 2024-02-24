import { VuetifyWidgetModel } from './VuetifyWidget';

export class DividerModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'DividerModel',
                dark: null,
                inset: null,
                light: null,
                vertical: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-divider';
    }
}

DividerModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
