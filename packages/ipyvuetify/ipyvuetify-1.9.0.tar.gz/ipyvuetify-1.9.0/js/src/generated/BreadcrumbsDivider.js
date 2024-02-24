import { VuetifyWidgetModel } from './VuetifyWidget';

export class BreadcrumbsDividerModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'BreadcrumbsDividerModel',
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-breadcrumbs-divider';
    }
}

BreadcrumbsDividerModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
