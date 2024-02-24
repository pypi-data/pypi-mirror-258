import { VuetifyWidgetModel } from './VuetifyWidget';

export class CounterModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'CounterModel',
                dark: null,
                light: null,
                max: undefined,
                value: undefined,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-counter';
    }
}

CounterModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
