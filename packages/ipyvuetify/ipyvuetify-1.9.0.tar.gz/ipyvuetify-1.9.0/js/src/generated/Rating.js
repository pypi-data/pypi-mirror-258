import { VuetifyWidgetModel } from './VuetifyWidget';

export class RatingModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'RatingModel',
                background_color: null,
                clearable: null,
                close_delay: undefined,
                color: null,
                dark: null,
                dense: null,
                empty_icon: null,
                full_icon: null,
                half_icon: null,
                half_increments: null,
                hover: null,
                large: null,
                length: undefined,
                light: null,
                open_delay: undefined,
                readonly: null,
                ripple: undefined,
                size: undefined,
                small: null,
                value: null,
                x_large: null,
                x_small: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-rating';
    }
}

RatingModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
