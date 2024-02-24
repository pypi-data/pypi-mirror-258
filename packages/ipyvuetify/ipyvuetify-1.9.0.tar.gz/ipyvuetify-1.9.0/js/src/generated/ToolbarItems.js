import { VuetifyWidgetModel } from './VuetifyWidget';

export class ToolbarItemsModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'ToolbarItemsModel',
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-toolbar-items';
    }
}

ToolbarItemsModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
