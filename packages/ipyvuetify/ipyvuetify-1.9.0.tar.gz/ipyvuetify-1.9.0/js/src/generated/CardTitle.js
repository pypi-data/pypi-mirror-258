import { VuetifyWidgetModel } from './VuetifyWidget';

export class CardTitleModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'CardTitleModel',
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-card-title';
    }
}

CardTitleModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
