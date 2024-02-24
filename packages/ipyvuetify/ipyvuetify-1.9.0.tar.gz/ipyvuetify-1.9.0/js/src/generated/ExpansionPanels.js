import { VuetifyWidgetModel } from './VuetifyWidget';

export class ExpansionPanelsModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'ExpansionPanelsModel',
                accordion: null,
                active_class: null,
                dark: null,
                disabled: null,
                flat: null,
                focusable: null,
                hover: null,
                inset: null,
                light: null,
                mandatory: null,
                max: undefined,
                multiple: null,
                popout: null,
                readonly: null,
                tile: null,
                value: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-expansion-panels';
    }
}

ExpansionPanelsModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
