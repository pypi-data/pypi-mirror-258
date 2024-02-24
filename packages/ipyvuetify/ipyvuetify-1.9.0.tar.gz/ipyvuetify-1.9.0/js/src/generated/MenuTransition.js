import { VuetifyWidgetModel } from './VuetifyWidget';

export class MenuTransitionModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'MenuTransitionModel',
                group: null,
                hide_on_leave: null,
                leave_absolute: null,
                mode: null,
                origin: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-menu-transition';
    }
}

MenuTransitionModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
