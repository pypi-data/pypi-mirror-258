import { VuetifyWidgetModel } from './VuetifyWidget';

export class BottomNavigationModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'BottomNavigationModel',
                absolute: null,
                active_class: null,
                app: null,
                background_color: null,
                color: null,
                dark: null,
                fixed: null,
                grow: null,
                height: undefined,
                hide_on_scroll: null,
                horizontal: null,
                input_value: null,
                light: null,
                mandatory: null,
                max_height: undefined,
                max_width: undefined,
                min_height: undefined,
                min_width: undefined,
                scroll_target: null,
                scroll_threshold: undefined,
                shift: null,
                value: null,
                width: undefined,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-bottom-navigation';
    }
}

BottomNavigationModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
