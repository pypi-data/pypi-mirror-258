import { VuetifyWidgetModel } from './VuetifyWidget';

export class SlideGroupModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'SlideGroupModel',
                active_class: null,
                center_active: null,
                dark: null,
                light: null,
                mandatory: null,
                max: undefined,
                mobile_break_point: undefined,
                multiple: null,
                next_icon: null,
                prev_icon: null,
                show_arrows: null,
                value: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-slide-group';
    }
}

SlideGroupModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
