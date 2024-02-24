import { VuetifyWidgetModel } from './VuetifyWidget';

export class PaginationModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'PaginationModel',
                circle: null,
                color: null,
                dark: null,
                disabled: null,
                length: null,
                light: null,
                next_icon: null,
                prev_icon: null,
                total_visible: undefined,
                value: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-pagination';
    }
}

PaginationModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
