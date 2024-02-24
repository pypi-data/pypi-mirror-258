import { VuetifyWidgetModel } from './VuetifyWidget';

export class DialogModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'DialogModel',
                activator: null,
                attach: null,
                close_delay: undefined,
                content_class: null,
                dark: null,
                disabled: null,
                eager: null,
                fullscreen: null,
                hide_overlay: null,
                internal_activator: null,
                light: null,
                max_width: undefined,
                no_click_animation: null,
                open_delay: undefined,
                open_on_hover: null,
                origin: null,
                overlay_color: null,
                overlay_opacity: undefined,
                persistent: null,
                retain_focus: null,
                return_value: null,
                scrollable: null,
                transition: undefined,
                value: null,
                width: undefined,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-dialog';
    }
}

DialogModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
