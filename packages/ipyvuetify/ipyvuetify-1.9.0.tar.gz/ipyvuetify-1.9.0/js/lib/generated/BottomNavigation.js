function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

import { VuetifyWidgetModel } from './VuetifyWidget';
export class BottomNavigationModel extends VuetifyWidgetModel {
  defaults() {
    return _objectSpread({}, super.defaults(), {
      _model_name: 'BottomNavigationModel',
      absolute: null,
      active_class: null,
      app: null,
      background_color: null,
      color: null,
      dark: null,
      fixed: null,
      grow: null,
      height: undefined,
      hide_on_scroll: null,
      horizontal: null,
      input_value: null,
      light: null,
      mandatory: null,
      max_height: undefined,
      max_width: undefined,
      min_height: undefined,
      min_width: undefined,
      scroll_target: null,
      scroll_threshold: undefined,
      shift: null,
      value: null,
      width: undefined
    });
  }

  getVueTag() {
    // eslint-disable-line class-methods-use-this
    return 'v-bottom-navigation';
  }

}
BottomNavigationModel.serializers = _objectSpread({}, VuetifyWidgetModel.serializers);