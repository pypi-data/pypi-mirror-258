import { VuetifyWidgetModel } from './VuetifyWidget';

export class ExpandTransitionModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'ExpandTransitionModel',
                mode: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-expand-transition';
    }
}

ExpandTransitionModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
