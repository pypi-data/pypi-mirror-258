import { VuetifyWidgetModel } from './VuetifyWidget';

export class BottomSheetModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'BottomSheetModel',
                activator: null,
                attach: null,
                close_delay: undefined,
                content_class: null,
                dark: null,
                disabled: null,
                eager: null,
                fullscreen: null,
                hide_overlay: null,
                inset: null,
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
                transition: null,
                value: null,
                width: undefined,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-bottom-sheet';
    }
}

BottomSheetModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
