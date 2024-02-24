function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

import { VuetifyWidgetModel } from './VuetifyWidget';
export class DataFooterModel extends VuetifyWidgetModel {
  defaults() {
    return _objectSpread({}, super.defaults(), {
      _model_name: 'DataFooterModel',
      disable_items_per_page: null,
      disable_pagination: null,
      first_icon: null,
      items_per_page_all_text: null,
      items_per_page_options: null,
      items_per_page_text: null,
      last_icon: null,
      next_icon: null,
      options: null,
      page_text: null,
      pagination: null,
      prev_icon: null,
      show_current_page: null,
      show_first_last_page: null
    });
  }

  getVueTag() {
    // eslint-disable-line class-methods-use-this
    return 'v-data-footer';
  }

}
DataFooterModel.serializers = _objectSpread({}, VuetifyWidgetModel.serializers);