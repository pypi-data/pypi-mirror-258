import { VuetifyWidgetModel } from './VuetifyWidget';

export class FabTransitionModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'FabTransitionModel',
                group: null,
                hide_on_leave: null,
                leave_absolute: null,
                mode: null,
                origin: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-fab-transition';
    }
}

FabTransitionModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
