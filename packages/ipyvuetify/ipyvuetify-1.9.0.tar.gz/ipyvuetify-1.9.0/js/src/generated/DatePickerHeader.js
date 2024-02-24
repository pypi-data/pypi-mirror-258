import { VuetifyWidgetModel } from './VuetifyWidget';

export class DatePickerHeaderModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'DatePickerHeaderModel',
                color: null,
                dark: null,
                disabled: null,
                light: null,
                locale: null,
                max: null,
                min: null,
                next_icon: null,
                prev_icon: null,
                readonly: null,
                value: undefined,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-date-picker-header';
    }
}

DatePickerHeaderModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
