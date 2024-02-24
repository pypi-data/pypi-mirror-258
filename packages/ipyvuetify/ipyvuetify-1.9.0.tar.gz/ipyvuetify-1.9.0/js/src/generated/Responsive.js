import { VuetifyWidgetModel } from './VuetifyWidget';

export class ResponsiveModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'ResponsiveModel',
                aspect_ratio: undefined,
                height: undefined,
                max_height: undefined,
                max_width: undefined,
                min_height: undefined,
                min_width: undefined,
                width: undefined,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-responsive';
    }
}

ResponsiveModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
