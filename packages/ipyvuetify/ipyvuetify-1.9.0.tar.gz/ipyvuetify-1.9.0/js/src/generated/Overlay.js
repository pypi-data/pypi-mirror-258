import { VuetifyWidgetModel } from './VuetifyWidget';

export class OverlayModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'OverlayModel',
                absolute: null,
                color: null,
                dark: null,
                light: null,
                opacity: undefined,
                value: null,
                z_index: undefined,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-overlay';
    }
}

OverlayModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
