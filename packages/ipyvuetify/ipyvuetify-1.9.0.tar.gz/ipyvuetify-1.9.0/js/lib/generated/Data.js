function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

import { VuetifyWidgetModel } from './VuetifyWidget';
export class DataModel extends VuetifyWidgetModel {
  defaults() {
    return _objectSpread({}, super.defaults(), {
      _model_name: 'DataModel',
      disable_filtering: null,
      disable_pagination: null,
      disable_sort: null,
      group_by: undefined,
      group_desc: undefined,
      items: null,
      items_per_page: null,
      locale: null,
      multi_sort: null,
      must_sort: null,
      options: null,
      page: null,
      search: null,
      server_items_length: null,
      sort_by: undefined,
      sort_desc: undefined
    });
  }

  getVueTag() {
    // eslint-disable-line class-methods-use-this
    return 'v-data';
  }

}
DataModel.serializers = _objectSpread({}, VuetifyWidgetModel.serializers);