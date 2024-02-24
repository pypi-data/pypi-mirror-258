import { VuetifyWidgetModel } from './VuetifyWidget';

export class ListItemGroupModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'ListItemGroupModel',
                active_class: null,
                color: null,
                dark: null,
                light: null,
                mandatory: null,
                max: undefined,
                multiple: null,
                value: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-list-item-group';
    }
}

ListItemGroupModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
