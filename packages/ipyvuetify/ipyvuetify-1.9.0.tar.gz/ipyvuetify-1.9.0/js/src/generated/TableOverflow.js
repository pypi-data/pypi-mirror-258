import { VuetifyWidgetModel } from './VuetifyWidget';

export class TableOverflowModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'TableOverflowModel',
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-table-overflow';
    }
}

TableOverflowModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
