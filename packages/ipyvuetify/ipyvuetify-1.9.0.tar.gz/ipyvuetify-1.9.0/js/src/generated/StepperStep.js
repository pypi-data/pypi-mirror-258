import { VuetifyWidgetModel } from './VuetifyWidget';

export class StepperStepModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'StepperStepModel',
                color: null,
                complete: null,
                complete_icon: null,
                edit_icon: null,
                editable: null,
                error_icon: null,
                rules: null,
                step: undefined,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-stepper-step';
    }
}

StepperStepModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
