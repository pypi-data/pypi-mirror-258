import { VuetifyWidgetModel } from './VuetifyWidget';

export class NavigationDrawerModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'NavigationDrawerModel',
                absolute: null,
                app: null,
                bottom: null,
                clipped: null,
                color: null,
                dark: null,
                disable_resize_watcher: null,
                disable_route_watcher: null,
                expand_on_hover: null,
                fixed: null,
                floating: null,
                height: undefined,
                hide_overlay: null,
                light: null,
                mini_variant: null,
                mini_variant_width: undefined,
                mobile_break_point: undefined,
                overlay_color: null,
                overlay_opacity: undefined,
                permanent: null,
                right: null,
                src: undefined,
                stateless: null,
                tag: null,
                temporary: null,
                touchless: null,
                value: null,
                width: undefined,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-navigation-drawer';
    }
}

NavigationDrawerModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
