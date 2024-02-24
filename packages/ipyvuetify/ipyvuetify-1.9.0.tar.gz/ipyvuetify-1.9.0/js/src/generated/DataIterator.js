import { VuetifyWidgetModel } from './VuetifyWidget';

export class DataIteratorModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'DataIteratorModel',
                dark: null,
                disable_filtering: null,
                disable_pagination: null,
                disable_sort: null,
                expanded: null,
                footer_props: null,
                group_by: undefined,
                group_desc: undefined,
                hide_default_footer: null,
                item_key: null,
                items: null,
                items_per_page: null,
                light: null,
                loading: undefined,
                loading_text: null,
                locale: null,
                mobile_breakpoint: undefined,
                multi_sort: null,
                must_sort: null,
                no_data_text: null,
                no_results_text: null,
                options: null,
                page: null,
                search: null,
                selectable_key: null,
                server_items_length: null,
                single_expand: null,
                single_select: null,
                sort_by: undefined,
                sort_desc: undefined,
                value: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-data-iterator';
    }
}

DataIteratorModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
