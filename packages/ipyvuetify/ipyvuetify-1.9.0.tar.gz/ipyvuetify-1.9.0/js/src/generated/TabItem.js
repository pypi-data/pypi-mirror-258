import { VuetifyWidgetModel } from './VuetifyWidget';

export class TabItemModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'TabItemModel',
                active_class: null,
                disabled: null,
                eager: null,
                id: null,
                reverse_transition: undefined,
                transition: undefined,
                value: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-tab-item';
    }
}

TabItemModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
