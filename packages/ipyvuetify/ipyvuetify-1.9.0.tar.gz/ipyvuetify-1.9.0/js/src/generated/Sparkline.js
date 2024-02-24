import { VuetifyWidgetModel } from './VuetifyWidget';

export class SparklineModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'SparklineModel',
                auto_draw: null,
                auto_draw_duration: null,
                auto_draw_easing: null,
                auto_line_width: null,
                color: null,
                fill: null,
                gradient: null,
                gradient_direction: null,
                height: undefined,
                label_size: undefined,
                labels: null,
                line_width: undefined,
                padding: undefined,
                show_labels: null,
                smooth: undefined,
                type: null,
                value: null,
                width: undefined,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-sparkline';
    }
}

SparklineModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
