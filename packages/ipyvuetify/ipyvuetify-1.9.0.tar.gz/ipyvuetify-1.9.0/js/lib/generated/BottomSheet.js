function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

import { VuetifyWidgetModel } from './VuetifyWidget';
export class BottomSheetModel extends VuetifyWidgetModel {
  defaults() {
    return _objectSpread({}, super.defaults(), {
      _model_name: 'BottomSheetModel',
      activator: null,
      attach: null,
      close_delay: undefined,
      content_class: null,
      dark: null,
      disabled: null,
      eager: null,
      fullscreen: null,
      hide_overlay: null,
      inset: null,
      internal_activator: null,
      light: null,
      max_width: undefined,
      no_click_animation: null,
      open_delay: undefined,
      open_on_hover: null,
      origin: null,
      overlay_color: null,
      overlay_opacity: undefined,
      persistent: null,
      retain_focus: null,
      return_value: null,
      scrollable: null,
      transition: null,
      value: null,
      width: undefined
    });
  }

  getVueTag() {
    // eslint-disable-line class-methods-use-this
    return 'v-bottom-sheet';
  }

}
BottomSheetModel.serializers = _objectSpread({}, VuetifyWidgetModel.serializers);