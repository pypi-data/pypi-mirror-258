function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

import { VuetifyWidgetModel } from './VuetifyWidget';
export class WindowModel extends VuetifyWidgetModel {
  defaults() {
    return _objectSpread({}, super.defaults(), {
      _model_name: 'WindowModel',
      active_class: null,
      continuous: null,
      dark: null,
      light: null,
      mandatory: null,
      max: undefined,
      multiple: null,
      next_icon: undefined,
      prev_icon: undefined,
      reverse: null,
      show_arrows: null,
      show_arrows_on_hover: null,
      touch: null,
      touchless: null,
      value: null,
      vertical: null
    });
  }

  getVueTag() {
    // eslint-disable-line class-methods-use-this
    return 'v-window';
  }

}
WindowModel.serializers = _objectSpread({}, VuetifyWidgetModel.serializers);