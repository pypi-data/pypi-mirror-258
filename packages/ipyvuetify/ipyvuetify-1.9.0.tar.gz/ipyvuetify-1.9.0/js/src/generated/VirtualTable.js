import { VuetifyWidgetModel } from './VuetifyWidget';

export class VirtualTableModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'VirtualTableModel',
                chunk_size: null,
                dark: null,
                dense: null,
                fixed_header: null,
                header_height: null,
                height: undefined,
                items: null,
                light: null,
                row_height: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-virtual-table';
    }
}

VirtualTableModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
