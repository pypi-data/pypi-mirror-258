import { VuetifyWidgetModel } from './VuetifyWidget';

export class StepperItemsModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'StepperItemsModel',
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-stepper-items';
    }
}

StepperItemsModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
