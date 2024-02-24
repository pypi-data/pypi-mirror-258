import { VuetifyWidgetModel } from './VuetifyWidget';

export class SlideXTransitionModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'SlideXTransitionModel',
                group: null,
                hide_on_leave: null,
                leave_absolute: null,
                mode: null,
                origin: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-slidex-transition';
    }
}

SlideXTransitionModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
