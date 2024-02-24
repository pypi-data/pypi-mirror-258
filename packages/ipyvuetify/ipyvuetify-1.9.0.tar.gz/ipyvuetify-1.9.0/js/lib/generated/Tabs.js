function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

import { VuetifyWidgetModel } from './VuetifyWidget';
export class TabsModel extends VuetifyWidgetModel {
  defaults() {
    return _objectSpread({}, super.defaults(), {
      _model_name: 'TabsModel',
      active_class: null,
      align_with_title: null,
      background_color: null,
      center_active: null,
      centered: null,
      color: null,
      dark: null,
      fixed_tabs: null,
      grow: null,
      height: undefined,
      hide_slider: null,
      icons_and_text: null,
      light: null,
      mobile_break_point: undefined,
      next_icon: null,
      optional: null,
      prev_icon: null,
      right: null,
      show_arrows: null,
      slider_color: null,
      slider_size: undefined,
      value: null,
      vertical: null
    });
  }

  getVueTag() {
    // eslint-disable-line class-methods-use-this
    return 'v-tabs';
  }

}
TabsModel.serializers = _objectSpread({}, VuetifyWidgetModel.serializers);