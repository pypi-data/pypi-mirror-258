import { VuetifyWidgetModel } from './VuetifyWidget';

export class AvatarModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'AvatarModel',
                color: null,
                height: undefined,
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
        return 'v-avatar';
    }
}

AvatarModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
