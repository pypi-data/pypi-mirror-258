import { VuetifyWidgetModel } from './VuetifyWidget';

export class DatePickerMonthTableModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'DatePickerMonthTableModel',
                color: null,
                current: null,
                dark: null,
                disabled: null,
                event_color: undefined,
                events: undefined,
                light: null,
                locale: null,
                max: null,
                min: null,
                range: null,
                readonly: null,
                scrollable: null,
                table_date: null,
                value: undefined,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-date-picker-month-table';
    }
}

DatePickerMonthTableModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
