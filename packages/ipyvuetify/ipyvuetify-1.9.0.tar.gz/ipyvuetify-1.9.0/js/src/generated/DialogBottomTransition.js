import { VuetifyWidgetModel } from './VuetifyWidget';

export class DialogBottomTransitionModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'DialogBottomTransitionModel',
                group: null,
                hide_on_leave: null,
                leave_absolute: null,
                mode: null,
                origin: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-dialog-bottom-transition';
    }
}

DialogBottomTransitionModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
