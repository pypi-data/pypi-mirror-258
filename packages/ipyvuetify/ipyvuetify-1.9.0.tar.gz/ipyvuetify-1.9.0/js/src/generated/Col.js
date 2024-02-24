import { VuetifyWidgetModel } from './VuetifyWidget';

export class ColModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'ColModel',
                align_self: null,
                cols: undefined,
                lg: undefined,
                md: undefined,
                offset: undefined,
                offset_lg: undefined,
                offset_md: undefined,
                offset_sm: undefined,
                offset_xl: undefined,
                order: undefined,
                order_lg: undefined,
                order_md: undefined,
                order_sm: undefined,
                order_xl: undefined,
                sm: undefined,
                tag: null,
                xl: undefined,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-col';
    }
}

ColModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
