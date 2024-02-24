import { VuetifyWidgetModel } from './VuetifyWidget';

export class BreadcrumbsItemModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'BreadcrumbsItemModel',
                active_class: null,
                append: null,
                disabled: null,
                exact: null,
                exact_active_class: null,
                href: undefined,
                link: null,
                nuxt: null,
                replace: null,
                ripple: undefined,
                tag: null,
                target: null,
                to: undefined,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-breadcrumbs-item';
    }
}

BreadcrumbsItemModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
