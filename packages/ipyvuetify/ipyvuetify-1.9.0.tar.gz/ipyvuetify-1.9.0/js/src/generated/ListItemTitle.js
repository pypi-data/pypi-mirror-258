import { VuetifyWidgetModel } from './VuetifyWidget';

export class ListItemTitleModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'ListItemTitleModel',
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-list-item-title';
    }
}

ListItemTitleModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
