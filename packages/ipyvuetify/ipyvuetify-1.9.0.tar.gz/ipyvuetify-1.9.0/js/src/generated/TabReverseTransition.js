import { VuetifyWidgetModel } from './VuetifyWidget';

export class TabReverseTransitionModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'TabReverseTransitionModel',
                group: null,
                hide_on_leave: null,
                leave_absolute: null,
                mode: null,
                origin: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-tab-reverse-transition';
    }
}

TabReverseTransitionModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
