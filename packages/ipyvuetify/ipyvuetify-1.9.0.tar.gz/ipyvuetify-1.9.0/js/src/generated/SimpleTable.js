import { VuetifyWidgetModel } from './VuetifyWidget';

export class SimpleTableModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'SimpleTableModel',
                dark: null,
                dense: null,
                fixed_header: null,
                height: undefined,
                light: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-simple-table';
    }
}

SimpleTableModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
