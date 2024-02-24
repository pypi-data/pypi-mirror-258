import { VuetifyWidgetModel } from './VuetifyWidget';

export class CardModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'CardModel',
                active_class: null,
                append: null,
                color: null,
                dark: null,
                disabled: null,
                elevation: undefined,
                exact: null,
                exact_active_class: null,
                flat: null,
                height: undefined,
                hover: null,
                href: undefined,
                img: null,
                light: null,
                link: null,
                loader_height: undefined,
                loading: undefined,
                max_height: undefined,
                max_width: undefined,
                min_height: undefined,
                min_width: undefined,
                nuxt: null,
                outlined: null,
                raised: null,
                replace: null,
                ripple: undefined,
                shaped: null,
                tag: null,
                target: null,
                tile: null,
                to: undefined,
                width: undefined,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-card';
    }
}

CardModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
