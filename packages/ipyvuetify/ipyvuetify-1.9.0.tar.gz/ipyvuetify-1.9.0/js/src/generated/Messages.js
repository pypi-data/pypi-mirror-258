import { VuetifyWidgetModel } from './VuetifyWidget';

export class MessagesModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'MessagesModel',
                color: null,
                dark: null,
                light: null,
                value: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-messages';
    }
}

MessagesModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
