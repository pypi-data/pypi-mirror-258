import { VuetifyWidgetModel } from './VuetifyWidget';

export class RadioGroupModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'RadioGroupModel',
                active_class: null,
                append_icon: null,
                background_color: null,
                color: null,
                column: null,
                dark: null,
                dense: null,
                disabled: null,
                error: null,
                error_count: undefined,
                error_messages: undefined,
                height: undefined,
                hide_details: undefined,
                hint: null,
                id: null,
                label: null,
                light: null,
                loading: null,
                mandatory: null,
                max: undefined,
                messages: undefined,
                multiple: null,
                name: null,
                persistent_hint: null,
                prepend_icon: null,
                readonly: null,
                row: null,
                rules: null,
                success: null,
                success_messages: undefined,
                validate_on_blur: null,
                value: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-radio-group';
    }
}

RadioGroupModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
