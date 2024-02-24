import { VuetifyWidgetModel } from './VuetifyWidget';

export class ScrollXTransitionModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'ScrollXTransitionModel',
                group: null,
                hide_on_leave: null,
                leave_absolute: null,
                mode: null,
                origin: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-scrollx-transition';
    }
}

ScrollXTransitionModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
