import { VuetifyWidgetModel } from './VuetifyWidget';

export class PickerModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'PickerModel',
                color: null,
                dark: null,
                full_width: null,
                landscape: null,
                light: null,
                no_title: null,
                transition: null,
                width: undefined,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-picker';
    }
}

PickerModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
