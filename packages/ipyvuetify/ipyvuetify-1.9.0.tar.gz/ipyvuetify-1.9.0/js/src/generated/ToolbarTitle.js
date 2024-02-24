import { VuetifyWidgetModel } from './VuetifyWidget';

export class ToolbarTitleModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'ToolbarTitleModel',
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-toolbar-title';
    }
}

ToolbarTitleModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
