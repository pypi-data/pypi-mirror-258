import { VuetifyWidgetModel } from './VuetifyWidget';

export class ScrollYTransitionModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'ScrollYTransitionModel',
                group: null,
                hide_on_leave: null,
                leave_absolute: null,
                mode: null,
                origin: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-scrolly-transition';
    }
}

ScrollYTransitionModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
