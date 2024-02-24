import { VuetifyWidgetModel } from './VuetifyWidget';

export class ListItemActionModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'ListItemActionModel',
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-list-item-action';
    }
}

ListItemActionModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
