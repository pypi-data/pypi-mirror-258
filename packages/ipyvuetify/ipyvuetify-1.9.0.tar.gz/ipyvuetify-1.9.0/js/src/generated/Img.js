import { VuetifyWidgetModel } from './VuetifyWidget';

export class ImgModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'ImgModel',
                alt: null,
                aspect_ratio: undefined,
                contain: null,
                eager: null,
                gradient: null,
                height: undefined,
                lazy_src: null,
                max_height: undefined,
                max_width: undefined,
                min_height: undefined,
                min_width: undefined,
                options: null,
                position: null,
                sizes: null,
                src: undefined,
                srcset: null,
                transition: undefined,
                width: undefined,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-img';
    }
}

ImgModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
