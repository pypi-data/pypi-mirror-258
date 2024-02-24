import { VuetifyWidgetModel } from './VuetifyWidget';

export class TimePickerClockModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'TimePickerClockModel',
                ampm: null,
                color: null,
                dark: null,
                disabled: null,
                double: null,
                light: null,
                max: null,
                min: null,
                readonly: null,
                rotate: null,
                scrollable: null,
                step: null,
                value: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-time-picker-clock';
    }
}

TimePickerClockModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
