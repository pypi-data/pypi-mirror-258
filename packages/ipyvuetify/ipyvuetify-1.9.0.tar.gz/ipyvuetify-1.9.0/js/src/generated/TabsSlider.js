import { VuetifyWidgetModel } from './VuetifyWidget';

export class TabsSliderModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'TabsSliderModel',
                color: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-tabs-slider';
    }
}

TabsSliderModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
