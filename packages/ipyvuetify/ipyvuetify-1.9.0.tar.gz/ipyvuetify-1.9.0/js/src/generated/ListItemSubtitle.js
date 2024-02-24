import { VuetifyWidgetModel } from './VuetifyWidget';

export class ListItemSubtitleModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'ListItemSubtitleModel',
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-list-item-subtitle';
    }
}

ListItemSubtitleModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
