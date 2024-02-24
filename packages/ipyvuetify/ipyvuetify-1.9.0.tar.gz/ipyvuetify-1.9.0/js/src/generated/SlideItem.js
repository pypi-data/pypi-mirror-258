import { VuetifyWidgetModel } from './VuetifyWidget';

export class SlideItemModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'SlideItemModel',
                active_class: null,
                disabled: null,
                value: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-slide-item';
    }
}

SlideItemModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
