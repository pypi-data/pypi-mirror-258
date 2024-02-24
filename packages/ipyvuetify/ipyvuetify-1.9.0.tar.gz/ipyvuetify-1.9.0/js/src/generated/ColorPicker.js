import { VuetifyWidgetModel } from './VuetifyWidget';

export class ColorPickerModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'ColorPickerModel',
                canvas_height: undefined,
                dark: null,
                disabled: null,
                dot_size: undefined,
                flat: null,
                hide_canvas: null,
                hide_inputs: null,
                hide_mode_switch: null,
                light: null,
                mode: null,
                show_swatches: null,
                swatches: null,
                swatches_max_height: undefined,
                value: undefined,
                width: undefined,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-color-picker';
    }
}

ColorPickerModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
