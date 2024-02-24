import { VuetifyWidgetModel } from './VuetifyWidget';

export class ListModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'ListModel',
                color: null,
                dark: null,
                dense: null,
                disabled: null,
                elevation: undefined,
                expand: null,
                flat: null,
                height: undefined,
                light: null,
                max_height: undefined,
                max_width: undefined,
                min_height: undefined,
                min_width: undefined,
                nav: null,
                rounded: null,
                shaped: null,
                subheader: null,
                tag: null,
                three_line: null,
                tile: null,
                two_line: null,
                width: undefined,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-list';
    }
}

ListModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
