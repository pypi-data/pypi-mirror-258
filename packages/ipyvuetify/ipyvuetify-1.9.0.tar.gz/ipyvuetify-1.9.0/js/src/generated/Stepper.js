import { VuetifyWidgetModel } from './VuetifyWidget';

export class StepperModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'StepperModel',
                alt_labels: null,
                dark: null,
                light: null,
                non_linear: null,
                value: null,
                vertical: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-stepper';
    }
}

StepperModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
