import { VuetifyWidgetModel } from './VuetifyWidget';

export class ListItemAvatarModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'ListItemAvatarModel',
                color: null,
                height: undefined,
                horizontal: null,
                left: null,
                max_height: undefined,
                max_width: undefined,
                min_height: undefined,
                min_width: undefined,
                right: null,
                size: undefined,
                tile: null,
                width: undefined,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-list-item-avatar';
    }
}

ListItemAvatarModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
