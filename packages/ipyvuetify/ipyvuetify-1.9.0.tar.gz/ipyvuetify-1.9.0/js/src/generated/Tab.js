import { VuetifyWidgetModel } from './VuetifyWidget';

export class TabModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'TabModel',
                active_class: null,
                append: null,
                dark: null,
                disabled: null,
                exact: null,
                exact_active_class: null,
                href: undefined,
                light: null,
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
        return 'v-tab';
    }
}

TabModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
