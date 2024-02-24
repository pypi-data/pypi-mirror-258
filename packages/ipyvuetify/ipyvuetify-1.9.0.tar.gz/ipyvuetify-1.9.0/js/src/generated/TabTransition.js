import { VuetifyWidgetModel } from './VuetifyWidget';

export class TabTransitionModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'TabTransitionModel',
                group: null,
                hide_on_leave: null,
                leave_absolute: null,
                mode: null,
                origin: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-tab-transition';
    }
}

TabTransitionModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
