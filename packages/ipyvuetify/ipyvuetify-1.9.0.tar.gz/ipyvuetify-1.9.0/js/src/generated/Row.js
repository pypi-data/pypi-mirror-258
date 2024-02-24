import { VuetifyWidgetModel } from './VuetifyWidget';

export class RowModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'RowModel',
                align: null,
                align_content: null,
                align_content_lg: null,
                align_content_md: null,
                align_content_sm: null,
                align_content_xl: null,
                align_lg: null,
                align_md: null,
                align_sm: null,
                align_xl: null,
                dense: null,
                justify: null,
                justify_lg: null,
                justify_md: null,
                justify_sm: null,
                justify_xl: null,
                no_gutters: null,
                tag: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-row';
    }
}

RowModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
