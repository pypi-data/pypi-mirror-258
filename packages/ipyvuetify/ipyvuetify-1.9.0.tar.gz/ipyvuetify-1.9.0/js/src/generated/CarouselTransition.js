import { VuetifyWidgetModel } from './VuetifyWidget';

export class CarouselTransitionModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'CarouselTransitionModel',
                group: null,
                hide_on_leave: null,
                leave_absolute: null,
                mode: null,
                origin: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-carousel-transition';
    }
}

CarouselTransitionModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
