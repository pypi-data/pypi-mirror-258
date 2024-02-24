import { VuetifyWidgetModel } from './VuetifyWidget';

export class CalendarMonthlyModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'CalendarMonthlyModel',
                color: null,
                dark: null,
                end: null,
                hide_header: null,
                light: null,
                locale: null,
                min_weeks: null,
                now: null,
                short_months: null,
                short_weekdays: null,
                show_month_on_first: null,
                start: null,
                weekdays: undefined,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-calendar-monthly';
    }
}

CalendarMonthlyModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
