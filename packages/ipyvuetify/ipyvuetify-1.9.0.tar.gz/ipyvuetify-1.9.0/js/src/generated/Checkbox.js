import { VuetifyWidgetModel } from './VuetifyWidget';

export class CheckboxModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'CheckboxModel',
                append_icon: null,
                background_color: null,
                color: null,
                dark: null,
                dense: null,
                disabled: null,
                error: null,
                error_count: undefined,
                error_messages: undefined,
                false_value: null,
                height: undefined,
                hide_details: undefined,
                hint: null,
                id: null,
                indeterminate: null,
                indeterminate_icon: null,
                input_value: null,
                label: null,
                light: null,
                loading: null,
                messages: undefined,
                multiple: null,
                off_icon: null,
                on_icon: null,
                persistent_hint: null,
                prepend_icon: null,
                readonly: null,
                ripple: undefined,
                rules: null,
                success: null,
                success_messages: undefined,
                true_value: null,
                validate_on_blur: null,
                value: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-checkbox';
    }
}

CheckboxModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
