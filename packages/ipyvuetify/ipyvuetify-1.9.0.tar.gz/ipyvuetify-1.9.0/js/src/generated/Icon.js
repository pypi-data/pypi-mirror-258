import { VuetifyWidgetModel } from './VuetifyWidget';

export class IconModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'IconModel',
                color: null,
                dark: null,
                dense: null,
                disabled: null,
                large: null,
                left: null,
                light: null,
                right: null,
                size: undefined,
                small: null,
                tag: null,
                x_large: null,
                x_small: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-icon';
    }
}

IconModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
