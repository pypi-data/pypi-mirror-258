import { VuetifyWidgetModel } from './VuetifyWidget';

export class ListGroupModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'ListGroupModel',
                active_class: null,
                append_icon: null,
                color: null,
                disabled: null,
                eager: null,
                group: null,
                no_action: null,
                prepend_icon: null,
                ripple: undefined,
                sub_group: null,
                value: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-list-group';
    }
}

ListGroupModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
