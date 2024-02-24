function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

import { VuetifyWidgetModel } from './VuetifyWidget';
export class DataIteratorModel extends VuetifyWidgetModel {
  defaults() {
    return _objectSpread({}, super.defaults(), {
      _model_name: 'DataIteratorModel',
      dark: null,
      disable_filtering: null,
      disable_pagination: null,
      disable_sort: null,
      expanded: null,
      footer_props: null,
      group_by: undefined,
      group_desc: undefined,
      hide_default_footer: null,
      item_key: null,
      items: null,
      items_per_page: null,
      light: null,
      loading: undefined,
      loading_text: null,
      locale: null,
      mobile_breakpoint: undefined,
      multi_sort: null,
      must_sort: null,
      no_data_text: null,
      no_results_text: null,
      options: null,
      page: null,
      search: null,
      selectable_key: null,
      server_items_length: null,
      single_expand: null,
      single_select: null,
      sort_by: undefined,
      sort_desc: undefined,
      value: null
    });
  }

  getVueTag() {
    // eslint-disable-line class-methods-use-this
    return 'v-data-iterator';
  }

}
DataIteratorModel.serializers = _objectSpread({}, VuetifyWidgetModel.serializers);