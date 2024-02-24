import { VuetifyWidgetModel } from './VuetifyWidget';

export class AppBarNavIconModel extends VuetifyWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...{
                _model_name: 'AppBarNavIconModel',
            },
        };
    }

    getVueTag() { // eslint-disable-line class-methods-use-this
        return 'v-app-bar-nav-icon';
    }
}

AppBarNavIconModel.serializers = {
    ...VuetifyWidgetModel.serializers,
};
