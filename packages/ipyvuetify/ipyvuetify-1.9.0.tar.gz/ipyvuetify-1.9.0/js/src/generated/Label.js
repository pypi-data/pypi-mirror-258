import { VuetifyWidgetModel } from './VuetifyWidget';

export class LabelModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'LabelModel',
                absolute: null,
                color: null,
                dark: null,
                disabled: null,
                focused: null,
                for_: null,
                left: undefined,
                light: null,
                right: undefined,
                value: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-label';
    }
}

LabelModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
