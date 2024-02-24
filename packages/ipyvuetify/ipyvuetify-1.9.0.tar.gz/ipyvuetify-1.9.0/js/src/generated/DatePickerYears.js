import { VuetifyWidgetModel } from './VuetifyWidget';

export class DatePickerYearsModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'DatePickerYearsModel',
                color: null,
                locale: null,
                max: undefined,
                min: undefined,
                readonly: null,
                value: undefined,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-date-picker-years';
    }
}

DatePickerYearsModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
