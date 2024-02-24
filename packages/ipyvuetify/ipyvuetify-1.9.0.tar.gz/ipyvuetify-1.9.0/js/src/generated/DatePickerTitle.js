import { VuetifyWidgetModel } from './VuetifyWidget';

export class DatePickerTitleModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'DatePickerTitleModel',
                color: null,
                date: null,
                disabled: null,
                readonly: null,
                selecting_year: null,
                value: null,
                year: undefined,
                year_icon: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-date-picker-title';
    }
}

DatePickerTitleModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
