import { VuetifyWidgetModel } from './VuetifyWidget';

export class TabsModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'TabsModel',
                active_class: null,
                align_with_title: null,
                background_color: null,
                center_active: null,
                centered: null,
                color: null,
                dark: null,
                fixed_tabs: null,
                grow: null,
                height: undefined,
                hide_slider: null,
                icons_and_text: null,
                light: null,
                mobile_break_point: undefined,
                next_icon: null,
                optional: null,
                prev_icon: null,
                right: null,
                show_arrows: null,
                slider_color: null,
                slider_size: undefined,
                value: null,
                vertical: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-tabs';
    }
}

TabsModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
