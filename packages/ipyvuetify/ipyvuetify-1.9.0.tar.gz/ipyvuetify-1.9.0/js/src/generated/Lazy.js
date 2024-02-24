import { VuetifyWidgetModel } from './VuetifyWidget';

export class LazyModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'LazyModel',
                min_height: undefined,
                options: null,
                tag: null,
                transition: null,
                value: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-lazy';
    }
}

LazyModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
