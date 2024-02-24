import { VuetifyWidgetModel } from './VuetifyWidget';

export class SubheaderModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'SubheaderModel',
                dark: null,
                inset: null,
                light: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-subheader';
    }
}

SubheaderModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
