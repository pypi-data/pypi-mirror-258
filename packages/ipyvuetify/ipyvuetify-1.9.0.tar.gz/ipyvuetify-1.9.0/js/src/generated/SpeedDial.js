import { VuetifyWidgetModel } from './VuetifyWidget';

export class SpeedDialModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'SpeedDialModel',
                absolute: null,
                bottom: null,
                direction: null,
                fixed: null,
                left: null,
                mode: null,
                open_on_hover: null,
                origin: null,
                right: null,
                top: null,
                transition: null,
                value: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-speed-dial';
    }
}

SpeedDialModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
