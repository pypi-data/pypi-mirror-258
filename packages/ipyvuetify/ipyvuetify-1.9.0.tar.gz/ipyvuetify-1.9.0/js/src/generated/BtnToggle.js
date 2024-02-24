import { VuetifyWidgetModel } from './VuetifyWidget';

export class BtnToggleModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'BtnToggleModel',
                active_class: null,
                background_color: null,
                borderless: null,
                color: null,
                dark: null,
                dense: null,
                group: null,
                light: null,
                mandatory: null,
                max: undefined,
                multiple: null,
                rounded: null,
                shaped: null,
                tile: null,
                value: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-btn-toggle';
    }
}

BtnToggleModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
