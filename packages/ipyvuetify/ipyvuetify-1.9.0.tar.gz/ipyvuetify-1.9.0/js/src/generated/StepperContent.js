import { VuetifyWidgetModel } from './VuetifyWidget';

export class StepperContentModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'StepperContentModel',
                step: undefined,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-stepper-content';
    }
}

StepperContentModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
