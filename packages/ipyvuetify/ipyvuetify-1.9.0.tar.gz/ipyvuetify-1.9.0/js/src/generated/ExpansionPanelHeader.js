import { VuetifyWidgetModel } from './VuetifyWidget';

export class ExpansionPanelHeaderModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'ExpansionPanelHeaderModel',
                color: null,
                disable_icon_rotate: null,
                expand_icon: null,
                hide_actions: null,
                ripple: undefined,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-expansion-panel-header';
    }
}

ExpansionPanelHeaderModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
