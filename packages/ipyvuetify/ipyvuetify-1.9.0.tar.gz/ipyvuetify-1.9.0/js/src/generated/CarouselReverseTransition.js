import { VuetifyWidgetModel } from './VuetifyWidget';

export class CarouselReverseTransitionModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'CarouselReverseTransitionModel',
                group: null,
                hide_on_leave: null,
                leave_absolute: null,
                mode: null,
                origin: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-carousel-reverse-transition';
    }
}

CarouselReverseTransitionModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
