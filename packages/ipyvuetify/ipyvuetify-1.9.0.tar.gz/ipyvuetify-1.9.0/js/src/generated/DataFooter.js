import { VuetifyWidgetModel } from './VuetifyWidget';

export class DataFooterModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'DataFooterModel',
                disable_items_per_page: null,
                disable_pagination: null,
                first_icon: null,
                items_per_page_all_text: null,
                items_per_page_options: null,
                items_per_page_text: null,
                last_icon: null,
                next_icon: null,
                options: null,
                page_text: null,
                pagination: null,
                prev_icon: null,
                show_current_page: null,
                show_first_last_page: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-data-footer';
    }
}

DataFooterModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
