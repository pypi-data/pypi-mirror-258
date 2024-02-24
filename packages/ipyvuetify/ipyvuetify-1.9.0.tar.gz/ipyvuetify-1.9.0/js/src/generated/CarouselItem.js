import { VuetifyWidgetModel } from './VuetifyWidget';

export class CarouselItemModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'CarouselItemModel',
                active_class: null,
                append: null,
                disabled: null,
                eager: null,
                exact: null,
                exact_active_class: null,
                href: undefined,
                link: null,
                nuxt: null,
                replace: null,
                reverse_transition: undefined,
                ripple: undefined,
                tag: null,
                target: null,
                to: undefined,
                transition: undefined,
                value: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-carousel-item';
    }
}

CarouselItemModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
