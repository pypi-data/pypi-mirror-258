import { VuetifyWidgetModel } from './VuetifyWidget';

export class ScrollXReverseTransitionModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'ScrollXReverseTransitionModel',
                group: null,
                hide_on_leave: null,
                leave_absolute: null,
                mode: null,
                origin: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-scrollx-reverse-transition';
    }
}

ScrollXReverseTransitionModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
