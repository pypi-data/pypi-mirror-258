import { VuetifyWidgetModel } from './VuetifyWidget';

export class SlideXReverseTransitionModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'SlideXReverseTransitionModel',
                group: null,
                hide_on_leave: null,
                leave_absolute: null,
                mode: null,
                origin: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-slidex-reverse-transition';
    }
}

SlideXReverseTransitionModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
