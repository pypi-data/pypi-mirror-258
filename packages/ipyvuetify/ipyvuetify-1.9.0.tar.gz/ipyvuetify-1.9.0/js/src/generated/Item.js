import { VuetifyWidgetModel } from './VuetifyWidget';

export class ItemModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'ItemModel',
                active_class: null,
                disabled: null,
                value: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-item';
    }
}

ItemModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
