import { VuetifyWidgetModel } from './VuetifyWidget';

export class CardActionsModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'CardActionsModel',
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-card-actions';
    }
}

CardActionsModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
