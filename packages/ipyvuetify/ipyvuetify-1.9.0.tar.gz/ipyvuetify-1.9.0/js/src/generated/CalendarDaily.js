import { VuetifyWidgetModel } from './VuetifyWidget';

export class CalendarDailyModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'CalendarDailyModel',
                color: null,
                dark: null,
                end: null,
                first_interval: undefined,
                hide_header: null,
                interval_count: undefined,
                interval_height: undefined,
                interval_minutes: undefined,
                interval_width: undefined,
                light: null,
                locale: null,
                max_days: null,
                now: null,
                short_intervals: null,
                short_weekdays: null,
                start: null,
                weekdays: undefined,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-calendar-daily';
    }
}

CalendarDailyModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
