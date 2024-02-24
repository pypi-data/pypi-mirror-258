import { VuetifyWidgetModel } from './VuetifyWidget';

export class TooltipModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'TooltipModel',
                absolute: null,
                activator: null,
                allow_overflow: null,
                attach: null,
                bottom: null,
                close_delay: undefined,
                color: null,
                content_class: null,
                dark: null,
                disabled: null,
                eager: null,
                fixed: null,
                internal_activator: null,
                left: null,
                light: null,
                max_width: undefined,
                min_width: undefined,
                nudge_bottom: undefined,
                nudge_left: undefined,
                nudge_right: undefined,
                nudge_top: undefined,
                nudge_width: undefined,
                offset_overflow: null,
                open_delay: undefined,
                open_on_click: null,
                open_on_hover: null,
                position_x: null,
                position_y: null,
                right: null,
                tag: null,
                top: null,
                transition: null,
                value: null,
                z_index: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-tooltip';
    }
}

TooltipModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
