import { VuetifyWidgetModel } from './VuetifyWidget';

export class CardSubtitleModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'CardSubtitleModel',
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-card-subtitle';
    }
}

CardSubtitleModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
