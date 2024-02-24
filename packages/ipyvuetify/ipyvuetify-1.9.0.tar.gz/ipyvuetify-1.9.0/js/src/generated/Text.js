import { VuetifyWidgetModel } from './VuetifyWidget';

export class TextModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'TextModel',
                value: "",
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-text';
    }
}

TextModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
