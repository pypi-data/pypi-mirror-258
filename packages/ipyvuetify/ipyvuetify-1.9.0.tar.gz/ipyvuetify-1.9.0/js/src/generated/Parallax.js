import { VuetifyWidgetModel } from './VuetifyWidget';

export class ParallaxModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'ParallaxModel',
                alt: null,
                height: undefined,
                src: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-parallax';
    }
}

ParallaxModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
