import { VuetifyWidgetModel } from './VuetifyWidget';

export class BannerModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'BannerModel',
                app: null,
                color: null,
                dark: null,
                elevation: undefined,
                height: undefined,
                icon: null,
                icon_color: null,
                light: null,
                max_height: undefined,
                max_width: undefined,
                min_height: undefined,
                min_width: undefined,
                mobile_break_point: undefined,
                single_line: null,
                sticky: null,
                tag: null,
                tile: null,
                value: null,
                width: undefined,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-banner';
    }
}

BannerModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
