import { VuetifyWidgetModel } from './VuetifyWidget';

export class ProgressCircularModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'ProgressCircularModel',
                button: null,
                color: null,
                indeterminate: null,
                rotate: undefined,
                size: undefined,
                value: undefined,
                width: undefined,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-progress-circular';
    }
}

ProgressCircularModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
