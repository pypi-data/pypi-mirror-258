import { VuetifyWidgetModel } from './VuetifyWidget';

export class FadeTransitionModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'FadeTransitionModel',
                group: null,
                hide_on_leave: null,
                leave_absolute: null,
                mode: null,
                origin: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-fade-transition';
    }
}

FadeTransitionModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
