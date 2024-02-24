import { VuetifyWidgetModel } from './VuetifyWidget';

export class ListItemActionTextModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'ListItemActionTextModel',
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-list-item-action-text';
    }
}

ListItemActionTextModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
