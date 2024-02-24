import { VuetifyWidgetModel } from './VuetifyWidget';

export class CardTextModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'CardTextModel',
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-card-text';
    }
}

CardTextModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
