import { VuetifyWidgetModel } from './VuetifyWidget';

export class BtnModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'BtnModel',
                absolute: null,
                active_class: null,
                append: null,
                block: null,
                bottom: null,
                color: null,
                dark: null,
                depressed: null,
                disabled: null,
                elevation: undefined,
                exact: null,
                exact_active_class: null,
                fab: null,
                fixed: null,
                height: undefined,
                href: undefined,
                icon: null,
                input_value: null,
                large: null,
                left: null,
                light: null,
                link: null,
                loading: null,
                max_height: undefined,
                max_width: undefined,
                min_height: undefined,
                min_width: undefined,
                nuxt: null,
                outlined: null,
                replace: null,
                retain_focus_on_click: null,
                right: null,
                ripple: undefined,
                rounded: null,
                small: null,
                tag: null,
                target: null,
                text: null,
                tile: null,
                to: undefined,
                top: null,
                type: null,
                value: null,
                width: undefined,
                x_large: null,
                x_small: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-btn';
    }
}

BtnModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
