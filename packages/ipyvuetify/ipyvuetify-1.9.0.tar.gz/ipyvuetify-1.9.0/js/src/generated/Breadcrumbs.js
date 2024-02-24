import { VuetifyWidgetModel } from './VuetifyWidget';

export class BreadcrumbsModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'BreadcrumbsModel',
                dark: null,
                divider: null,
                items: null,
                large: null,
                light: null,
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-breadcrumbs';
    }
}

BreadcrumbsModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
