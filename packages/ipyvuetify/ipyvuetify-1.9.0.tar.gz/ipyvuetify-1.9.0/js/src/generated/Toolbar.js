import { VuetifyWidgetModel } from './VuetifyWidget';

export class ToolbarModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'ToolbarModel',
                absolute: null,
                bottom: null,
                collapse: null,
                color: null,
                dark: null,
                dense: null,
                elevation: undefined,
                extended: null,
                extension_height: undefined,
                flat: null,
                floating: null,
                height: undefined,
                light: null,
                max_height: undefined,
                max_width: undefined,
                min_height: undefined,
                min_width: undefined,
                prominent: null,
                short: null,
                src: undefined,
                tag: null,
                tile: null,
                width: undefined,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-toolbar';
    }
}

ToolbarModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
