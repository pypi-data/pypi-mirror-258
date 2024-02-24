import { VuetifyWidgetModel } from './VuetifyWidget';

export class HoverModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'HoverModel',
                close_delay: undefined,
                disabled: null,
                open_delay: undefined,
                value: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-hover';
    }
}

HoverModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
