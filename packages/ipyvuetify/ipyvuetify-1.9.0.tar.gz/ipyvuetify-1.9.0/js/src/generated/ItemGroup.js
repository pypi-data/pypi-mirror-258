import { VuetifyWidgetModel } from './VuetifyWidget';

export class ItemGroupModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'ItemGroupModel',
                active_class: null,
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
        return 'v-item-group';
    }
}

ItemGroupModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
