import { VuetifyWidgetModel } from './VuetifyWidget';

export class RangeSliderModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'RangeSliderModel',
                append_icon: null,
                background_color: null,
                color: null,
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
                inverse_label: null,
                label: null,
                light: null,
                loader_height: undefined,
                loading: undefined,
                max: undefined,
                messages: undefined,
                min: undefined,
                persistent_hint: null,
                prepend_icon: null,
                readonly: null,
                rules: null,
                step: undefined,
                success: null,
                success_messages: undefined,
                thumb_color: null,
                thumb_label: undefined,
                thumb_size: undefined,
                tick_labels: null,
                tick_size: undefined,
                ticks: undefined,
                track_color: null,
                track_fill_color: null,
                validate_on_blur: null,
                value: null,
                vertical: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-range-slider';
    }
}

RangeSliderModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
