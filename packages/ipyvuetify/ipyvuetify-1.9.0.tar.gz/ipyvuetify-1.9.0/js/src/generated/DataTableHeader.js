import { VuetifyWidgetModel } from './VuetifyWidget';

export class DataTableHeaderModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'DataTableHeaderModel',
                mobile: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-data-table-header';
    }
}

DataTableHeaderModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
