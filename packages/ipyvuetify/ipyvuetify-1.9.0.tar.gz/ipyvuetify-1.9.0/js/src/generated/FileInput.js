import { VuetifyWidgetModel } from './VuetifyWidget';

export class FileInputModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'FileInputModel',
                append_icon: null,
                append_outer_icon: null,
                autofocus: null,
                background_color: null,
                chips: null,
                clear_icon: null,
                clearable: null,
                color: null,
                counter: undefined,
                counter_size_string: null,
                counter_string: null,
                dark: null,
                dense: null,
                disabled: null,
                error: null,
                error_count: undefined,
                error_messages: undefined,
                filled: null,
                flat: null,
                full_width: null,
                height: undefined,
                hide_details: undefined,
                hint: null,
                id: null,
                label: null,
                light: null,
                loader_height: undefined,
                loading: undefined,
                messages: undefined,
                multiple: null,
                outlined: null,
                persistent_hint: null,
                placeholder: null,
                prefix: null,
                prepend_icon: null,
                prepend_inner_icon: null,
                readonly: null,
                reverse: null,
                rounded: null,
                rules: null,
                shaped: null,
                show_size: undefined,
                single_line: null,
                small_chips: null,
                solo: null,
                solo_inverted: null,
                success: null,
                success_messages: undefined,
                suffix: null,
                truncate_length: undefined,
                type: null,
                validate_on_blur: null,
                value: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-file-input';
    }
}

FileInputModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
