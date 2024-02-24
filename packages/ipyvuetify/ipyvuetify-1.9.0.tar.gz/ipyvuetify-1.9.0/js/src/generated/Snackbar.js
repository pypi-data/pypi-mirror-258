import { VuetifyWidgetModel } from './VuetifyWidget';

export class SnackbarModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'SnackbarModel',
                absolute: null,
                bottom: null,
                color: null,
                left: null,
                multi_line: null,
                right: null,
                timeout: null,
                top: null,
                value: null,
                vertical: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-snackbar';
    }
}

SnackbarModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
