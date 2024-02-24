import { VuetifyWidgetModel } from './VuetifyWidget';

export class TimelineItemModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'TimelineItemModel',
                color: null,
                dark: null,
                fill_dot: null,
                hide_dot: null,
                icon: null,
                icon_color: null,
                large: null,
                left: null,
                light: null,
                right: null,
                small: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-timeline-item';
    }
}

TimelineItemModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
