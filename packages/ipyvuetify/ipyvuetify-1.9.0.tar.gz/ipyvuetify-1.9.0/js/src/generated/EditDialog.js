import { VuetifyWidgetModel } from './VuetifyWidget';

export class EditDialogModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'EditDialogModel',
                cancel_text: null,
                dark: null,
                eager: null,
                large: null,
                light: null,
                persistent: null,
                return_value: null,
                save_text: null,
                transition: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-edit-dialog';
    }
}

EditDialogModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
