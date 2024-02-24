import { VuetifyWidgetModel } from './VuetifyWidget';

export class CalendarModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'CalendarModel',
                color: null,
                dark: null,
                end: null,
                event_color: undefined,
                event_end: null,
                event_height: null,
                event_margin_bottom: null,
                event_more: null,
                event_more_text: null,
                event_name: undefined,
                event_overlap_mode: undefined,
                event_overlap_threshold: undefined,
                event_ripple: undefined,
                event_start: null,
                event_text_color: undefined,
                events: null,
                first_interval: undefined,
                hide_header: null,
                interval_count: undefined,
                interval_height: undefined,
                interval_minutes: undefined,
                interval_width: undefined,
                light: null,
                locale: null,
                max_days: null,
                min_weeks: null,
                now: null,
                short_intervals: null,
                short_months: null,
                short_weekdays: null,
                show_month_on_first: null,
                start: null,
                type: null,
                value: null,
                weekdays: undefined,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-calendar';
    }
}

CalendarModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
