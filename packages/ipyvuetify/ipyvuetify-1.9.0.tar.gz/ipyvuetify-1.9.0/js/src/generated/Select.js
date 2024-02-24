import { VuetifyWidgetModel } from './VuetifyWidget';

export class SelectModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'SelectModel',
                append_icon: null,
                append_outer_icon: null,
                attach: null,
                autofocus: null,
                background_color: null,
                cache_items: null,
                chips: null,
                clear_icon: null,
                clearable: null,
                color: null,
                counter: undefined,
                dark: null,
                deletable_chips: null,
                dense: null,
                disable_lookup: null,
                disabled: null,
                eager: null,
                error: null,
                error_count: undefined,
                error_messages: undefined,
                filled: null,
                flat: null,
                full_width: null,
                height: undefined,
                hide_details: undefined,
                hide_selected: null,
                hint: null,
                id: null,
                item_color: null,
                item_disabled: undefined,
                item_text: undefined,
                item_value: undefined,
                items: null,
                label: null,
                light: null,
                loader_height: undefined,
                loading: undefined,
                menu_props: undefined,
                messages: undefined,
                multiple: null,
                no_data_text: null,
                open_on_clear: null,
                outlined: null,
                persistent_hint: null,
                placeholder: null,
                prefix: null,
                prepend_icon: null,
                prepend_inner_icon: null,
                readonly: null,
                return_object: null,
                reverse: null,
                rounded: null,
                rules: null,
                shaped: null,
                single_line: null,
                small_chips: null,
                solo: null,
                solo_inverted: null,
                success: null,
                success_messages: undefined,
                suffix: null,
                type: null,
                validate_on_blur: null,
                value: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-select';
    }
}

SelectModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
