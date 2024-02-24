import { VuetifyWidgetModel } from './VuetifyWidget';

export class SheetModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'SheetModel',
                color: null,
                dark: null,
                elevation: undefined,
                height: undefined,
                light: null,
                max_height: undefined,
                max_width: undefined,
                min_height: undefined,
                min_width: undefined,
                tag: null,
                tile: null,
                width: undefined,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-sheet';
    }
}

SheetModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
