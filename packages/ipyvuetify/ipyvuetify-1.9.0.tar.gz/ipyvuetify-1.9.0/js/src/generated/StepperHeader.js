import { VuetifyWidgetModel } from './VuetifyWidget';

export class StepperHeaderModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'StepperHeaderModel',
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-stepper-header';
    }
}

StepperHeaderModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
