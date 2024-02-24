import { VuetifyWidgetModel } from './VuetifyWidget';

export class ChipModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'ChipModel',
                active: null,
                active_class: null,
                append: null,
                close_: null,
                close_icon: null,
                color: null,
                dark: null,
                disabled: null,
                draggable: null,
                exact: null,
                exact_active_class: null,
                filter: null,
                filter_icon: null,
                href: undefined,
                input_value: null,
                label: null,
                large: null,
                light: null,
                link: null,
                nuxt: null,
                outlined: null,
                pill: null,
                replace: null,
                ripple: undefined,
                small: null,
                tag: null,
                target: null,
                text_color: null,
                to: undefined,
                value: null,
                x_large: null,
                x_small: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-chip';
    }
}

ChipModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
