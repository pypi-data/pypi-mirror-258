import { VuetifyWidgetModel } from './VuetifyWidget';

export class TimePickerModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'TimePickerModel',
                allowed_hours: undefined,
                allowed_minutes: undefined,
                allowed_seconds: undefined,
                ampm_in_title: null,
                color: null,
                dark: null,
                disabled: null,
                format: null,
                full_width: null,
                header_color: null,
                landscape: null,
                light: null,
                max: null,
                min: null,
                no_title: null,
                readonly: null,
                scrollable: null,
                use_seconds: null,
                value: null,
                width: undefined,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-time-picker';
    }
}

TimePickerModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
