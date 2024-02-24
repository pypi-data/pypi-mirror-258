import { VuetifyWidgetModel } from './VuetifyWidget';

export class ScrollYReverseTransitionModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'ScrollYReverseTransitionModel',
                group: null,
                hide_on_leave: null,
                leave_absolute: null,
                mode: null,
                origin: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-scrolly-reverse-transition';
    }
}

ScrollYReverseTransitionModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
