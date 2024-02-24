import { VuetifyWidgetModel } from './VuetifyWidget';

export class ColorPickerSwatchesModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'ColorPickerSwatchesModel',
                color: null,
                dark: null,
                light: null,
                max_height: undefined,
                max_width: undefined,
                swatches: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-color-picker-swatches';
    }
}

ColorPickerSwatchesModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
