import { VuetifyWidgetModel } from './VuetifyWidget';

export class SkeletonLoaderModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'SkeletonLoaderModel',
                boilerplate: null,
                dark: null,
                elevation: undefined,
                height: undefined,
                light: null,
                loading: null,
                max_height: undefined,
                max_width: undefined,
                min_height: undefined,
                min_width: undefined,
                tile: null,
                transition: null,
                type: null,
                types: null,
                width: undefined,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-skeleton-loader';
    }
}

SkeletonLoaderModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
