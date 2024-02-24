import { VuetifyWidgetModel } from './VuetifyWidget';

export class TimelineModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'TimelineModel',
                align_top: null,
                dark: null,
                dense: null,
                light: null,
                reverse: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-timeline';
    }
}

TimelineModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
