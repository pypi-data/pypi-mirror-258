import { VuetifyWidgetModel } from './VuetifyWidget';

export class BadgeModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'BadgeModel',
                avatar: null,
                bordered: null,
                bottom: null,
                color: null,
                content: null,
                dark: null,
                dot: null,
                icon: null,
                inline: null,
                label: null,
                left: null,
                light: null,
                mode: null,
                offset_x: undefined,
                offset_y: undefined,
                origin: null,
                overlap: null,
                tile: null,
                transition: null,
                value: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-badge';
    }
}

BadgeModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
