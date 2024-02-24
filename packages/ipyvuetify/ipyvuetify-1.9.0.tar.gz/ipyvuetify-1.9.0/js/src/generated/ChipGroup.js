import { VuetifyWidgetModel } from './VuetifyWidget';

export class ChipGroupModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'ChipGroupModel',
                active_class: null,
                center_active: null,
                color: null,
                column: null,
                dark: null,
                light: null,
                mandatory: null,
                max: undefined,
                mobile_break_point: undefined,
                multiple: null,
                next_icon: null,
                prev_icon: null,
                show_arrows: null,
                value: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-chip-group';
    }
}

ChipGroupModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
