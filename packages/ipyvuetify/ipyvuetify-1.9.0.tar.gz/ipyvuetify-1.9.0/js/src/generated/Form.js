import { VuetifyWidgetModel } from './VuetifyWidget';

export class FormModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'FormModel',
                lazy_validation: null,
                value: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-form';
    }
}

FormModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
