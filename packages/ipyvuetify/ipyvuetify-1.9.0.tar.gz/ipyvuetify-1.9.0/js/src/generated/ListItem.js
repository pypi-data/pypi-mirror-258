import { VuetifyWidgetModel } from './VuetifyWidget';

export class ListItemModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'ListItemModel',
                active_class: null,
                append: null,
                color: null,
                dark: null,
                dense: null,
                disabled: null,
                exact: null,
                exact_active_class: null,
                href: undefined,
                inactive: null,
                input_value: null,
                light: null,
                link: null,
                nuxt: null,
                replace: null,
                ripple: undefined,
                selectable: null,
                tag: null,
                target: null,
                three_line: null,
                to: undefined,
                two_line: null,
                value: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-list-item';
    }
}

ListItemModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
