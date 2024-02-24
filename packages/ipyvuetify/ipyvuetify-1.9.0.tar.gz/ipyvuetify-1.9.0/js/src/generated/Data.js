import { VuetifyWidgetModel } from './VuetifyWidget';

export class DataModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'DataModel',
                disable_filtering: null,
                disable_pagination: null,
                disable_sort: null,
                group_by: undefined,
                group_desc: undefined,
                items: null,
                items_per_page: null,
                locale: null,
                multi_sort: null,
                must_sort: null,
                options: null,
                page: null,
                search: null,
                server_items_length: null,
                sort_by: undefined,
                sort_desc: undefined,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-data';
    }
}

DataModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
