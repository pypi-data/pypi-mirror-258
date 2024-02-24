import { VuetifyWidgetModel } from './VuetifyWidget';

export class ExpandXTransitionModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'ExpandXTransitionModel',
                mode: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-expandx-transition';
    }
}

ExpandXTransitionModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
