import { VuetifyWidgetModel } from './VuetifyWidget';

export class DialogTransitionModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'DialogTransitionModel',
                group: null,
                hide_on_leave: null,
                leave_absolute: null,
                mode: null,
                origin: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-dialog-transition';
    }
}

DialogTransitionModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
