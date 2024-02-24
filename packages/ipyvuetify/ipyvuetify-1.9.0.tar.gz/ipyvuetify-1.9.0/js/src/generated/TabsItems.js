import { VuetifyWidgetModel } from './VuetifyWidget';

export class TabsItemsModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'TabsItemsModel',
                active_class: null,
                continuous: null,
                dark: null,
                light: null,
                mandatory: null,
                max: undefined,
                multiple: null,
                next_icon: undefined,
                prev_icon: undefined,
                reverse: null,
                show_arrows: null,
                show_arrows_on_hover: null,
                touch: null,
                touchless: null,
                value: null,
                vertical: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-tabs-items';
    }
}

TabsItemsModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
