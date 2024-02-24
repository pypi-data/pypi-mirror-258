import { VuetifyWidgetModel } from './VuetifyWidget';

export class TimePickerTitleModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'TimePickerTitleModel',
                ampm: null,
                ampm_readonly: null,
                color: null,
                disabled: null,
                hour: null,
                minute: null,
                period: null,
                readonly: null,
                second: null,
                selecting: null,
                use_seconds: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-time-picker-title';
    }
}

TimePickerTitleModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
