import { VuetifyWidgetModel } from './VuetifyWidget';

export class SlideYReverseTransitionModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'SlideYReverseTransitionModel',
                group: null,
                hide_on_leave: null,
                leave_absolute: null,
                mode: null,
                origin: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-slidey-reverse-transition';
    }
}

SlideYReverseTransitionModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
