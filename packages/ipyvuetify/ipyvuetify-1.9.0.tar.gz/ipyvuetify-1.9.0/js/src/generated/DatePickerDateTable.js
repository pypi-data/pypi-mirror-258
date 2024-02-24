import { VuetifyWidgetModel } from './VuetifyWidget';

export class DatePickerDateTableModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'DatePickerDateTableModel',
                color: null,
                current: null,
                dark: null,
                disabled: null,
                event_color: undefined,
                events: undefined,
                first_day_of_week: undefined,
                light: null,
                locale: null,
                locale_first_day_of_year: undefined,
                max: null,
                min: null,
                range: null,
                readonly: null,
                scrollable: null,
                show_week: null,
                table_date: null,
                value: undefined,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-date-picker-date-table';
    }
}

DatePickerDateTableModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
