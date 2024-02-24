import { VuetifyWidgetModel } from './VuetifyWidget';

export class SlideYTransitionModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'SlideYTransitionModel',
                group: null,
                hide_on_leave: null,
                leave_absolute: null,
                mode: null,
                origin: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-slidey-transition';
    }
}

SlideYTransitionModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
