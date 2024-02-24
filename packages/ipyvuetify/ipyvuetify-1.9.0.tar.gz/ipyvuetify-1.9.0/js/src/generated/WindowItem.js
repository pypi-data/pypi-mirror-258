import { VuetifyWidgetModel } from './VuetifyWidget';

export class WindowItemModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'WindowItemModel',
                active_class: null,
                disabled: null,
                eager: null,
                reverse_transition: undefined,
                transition: undefined,
                value: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-window-item';
    }
}

WindowItemModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
