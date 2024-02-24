import { VuetifyWidgetModel } from './VuetifyWidget';

export class ExpansionPanelModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'ExpansionPanelModel',
                active_class: null,
                disabled: null,
                readonly: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-expansion-panel';
    }
}

ExpansionPanelModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
