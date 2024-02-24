import { VuetifyWidgetModel } from './VuetifyWidget';

export class RadioModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'RadioModel',
                active_class: null,
                color: null,
                dark: null,
                disabled: null,
                id: null,
                label: null,
                light: null,
                name: null,
                off_icon: null,
                on_icon: null,
                readonly: null,
                ripple: undefined,
                value: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-radio';
    }
}

RadioModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
