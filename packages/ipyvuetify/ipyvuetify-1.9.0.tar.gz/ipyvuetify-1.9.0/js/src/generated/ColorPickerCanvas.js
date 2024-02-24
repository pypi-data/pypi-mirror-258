import { VuetifyWidgetModel } from './VuetifyWidget';

export class ColorPickerCanvasModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'ColorPickerCanvasModel',
                color: null,
                disabled: null,
                dot_size: undefined,
                height: undefined,
                width: undefined,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-color-picker-canvas';
    }
}

ColorPickerCanvasModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
