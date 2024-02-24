import { VuetifyWidgetModel } from './VuetifyWidget';

export class ProgressLinearModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'ProgressLinearModel',
                absolute: null,
                active: null,
                background_color: null,
                background_opacity: undefined,
                bottom: null,
                buffer_value: undefined,
                color: null,
                dark: null,
                fixed: null,
                height: undefined,
                indeterminate: null,
                light: null,
                query: null,
                rounded: null,
                stream: null,
                striped: null,
                top: null,
                value: undefined,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-progress-linear';
    }
}

ProgressLinearModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
