import { VuetifyWidgetModel } from './VuetifyWidget';

export class ExpansionPanelContentModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'ExpansionPanelContentModel',
                color: null,
                eager: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-expansion-panel-content';
    }
}

ExpansionPanelContentModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
