import { VuetifyWidgetModel } from './VuetifyWidget';

export class TreeviewNodeModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'TreeviewNodeModel',
                activatable: null,
                active_class: null,
                color: null,
                expand_icon: null,
                indeterminate_icon: null,
                item: null,
                item_children: null,
                item_disabled: null,
                item_key: null,
                item_text: null,
                level: null,
                loading_icon: null,
                off_icon: null,
                on_icon: null,
                open_on_click: null,
                rounded: null,
                selectable: null,
                selected_color: null,
                shaped: null,
                transition: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-treeview-node';
    }
}

TreeviewNodeModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
