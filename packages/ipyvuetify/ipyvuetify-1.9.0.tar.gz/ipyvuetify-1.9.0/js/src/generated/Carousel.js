import { VuetifyWidgetModel } from './VuetifyWidget';

export class CarouselModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'CarouselModel',
                active_class: null,
                continuous: null,
                cycle: null,
                dark: null,
                delimiter_icon: null,
                height: undefined,
                hide_delimiter_background: null,
                hide_delimiters: null,
                interval: undefined,
                light: null,
                mandatory: null,
                max: undefined,
                multiple: null,
                next_icon: undefined,
                prev_icon: undefined,
                progress: null,
                progress_color: null,
                reverse: null,
                show_arrows: null,
                show_arrows_on_hover: null,
                touch: null,
                touchless: null,
                value: null,
                vertical: null,
                vertical_delimiters: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-carousel';
    }
}

CarouselModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
