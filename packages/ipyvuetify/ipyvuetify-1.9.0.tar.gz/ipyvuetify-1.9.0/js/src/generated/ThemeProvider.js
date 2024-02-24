import { VuetifyWidgetModel } from './VuetifyWidget';

export class ThemeProviderModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'ThemeProviderModel',
                dark: null,
                light: null,
                root: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-theme-provider';
    }
}

ThemeProviderModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
