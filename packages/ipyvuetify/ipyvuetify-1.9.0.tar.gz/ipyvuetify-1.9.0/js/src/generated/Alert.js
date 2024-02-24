import { VuetifyWidgetModel } from './VuetifyWidget';

export class AlertModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'AlertModel',
                border: null,
                close_label: null,
                color: null,
                colored_border: null,
                dark: null,
                dense: null,
                dismissible: null,
                elevation: undefined,
                height: undefined,
                icon: undefined,
                light: null,
                max_height: undefined,
                max_width: undefined,
                min_height: undefined,
                min_width: undefined,
                mode: null,
                origin: null,
                outlined: null,
                prominent: null,
                tag: null,
                text: null,
                tile: null,
                transition: null,
                type: null,
                value: null,
                width: undefined,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-alert';
    }
}

AlertModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
