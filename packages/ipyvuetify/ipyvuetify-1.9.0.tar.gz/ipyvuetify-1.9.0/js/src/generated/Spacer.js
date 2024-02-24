import { VuetifyWidgetModel } from './VuetifyWidget';

export class SpacerModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'SpacerModel',
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-spacer';
    }
}

SpacerModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
