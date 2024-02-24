import { VuetifyWidgetModel } from './VuetifyWidget';

export class ListItemIconModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'ListItemIconModel',
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-list-item-icon';
    }
}

ListItemIconModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
