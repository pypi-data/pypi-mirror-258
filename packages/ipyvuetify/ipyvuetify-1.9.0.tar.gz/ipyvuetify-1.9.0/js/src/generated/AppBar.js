import { VuetifyWidgetModel } from './VuetifyWidget';

export class AppBarModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'AppBarModel',
                absolute: null,
                app: null,
                bottom: null,
                clipped_left: null,
                clipped_right: null,
                collapse: null,
                collapse_on_scroll: null,
                color: null,
                dark: null,
                dense: null,
                elevate_on_scroll: null,
                elevation: undefined,
                extended: null,
                extension_height: undefined,
                fade_img_on_scroll: null,
                fixed: null,
                flat: null,
                floating: null,
                height: undefined,
                hide_on_scroll: null,
                inverted_scroll: null,
                light: null,
                max_height: undefined,
                max_width: undefined,
                min_height: undefined,
                min_width: undefined,
                prominent: null,
                scroll_off_screen: null,
                scroll_target: null,
                scroll_threshold: undefined,
                short: null,
                shrink_on_scroll: null,
                src: undefined,
                tag: null,
                tile: null,
                value: null,
                width: undefined,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-app-bar';
    }
}

AppBarModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
