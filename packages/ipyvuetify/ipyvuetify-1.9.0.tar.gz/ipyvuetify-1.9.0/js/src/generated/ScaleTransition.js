import { VuetifyWidgetModel } from './VuetifyWidget';

export class ScaleTransitionModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'ScaleTransitionModel',
                group: null,
                hide_on_leave: null,
                leave_absolute: null,
                mode: null,
                origin: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-scale-transition';
    }
}

ScaleTransitionModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
