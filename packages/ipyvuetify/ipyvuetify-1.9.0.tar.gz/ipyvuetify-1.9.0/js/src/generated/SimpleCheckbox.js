import { VuetifyWidgetModel } from './VuetifyWidget';

export class SimpleCheckboxModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'SimpleCheckboxModel',
                color: null,
                dark: null,
                disabled: null,
                indeterminate: null,
                indeterminate_icon: null,
                light: null,
                off_icon: null,
                on_icon: null,
                ripple: null,
                value: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-simple-checkbox';
    }
}

SimpleCheckboxModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
