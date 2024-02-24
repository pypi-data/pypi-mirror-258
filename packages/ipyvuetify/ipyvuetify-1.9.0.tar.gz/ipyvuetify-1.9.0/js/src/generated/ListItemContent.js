import { VuetifyWidgetModel } from './VuetifyWidget';

export class ListItemContentModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'ListItemContentModel',
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-list-item-content';
    }
}

ListItemContentModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
