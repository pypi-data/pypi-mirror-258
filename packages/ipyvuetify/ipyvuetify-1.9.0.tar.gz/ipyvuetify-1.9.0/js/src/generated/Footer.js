import { VuetifyWidgetModel } from './VuetifyWidget';

export class FooterModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'FooterModel',
                absolute: null,
                app: null,
                color: null,
                dark: null,
                elevation: undefined,
                fixed: null,
                height: undefined,
                inset: null,
                light: null,
                max_height: undefined,
                max_width: undefined,
                min_height: undefined,
                min_width: undefined,
                padless: null,
                tag: null,
                tile: null,
                width: undefined,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-footer';
    }
}

FooterModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
