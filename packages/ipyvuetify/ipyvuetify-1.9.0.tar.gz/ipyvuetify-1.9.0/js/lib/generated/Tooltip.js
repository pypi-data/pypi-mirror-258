function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

import { VuetifyWidgetModel } from './VuetifyWidget';
export class TooltipModel extends VuetifyWidgetModel {
  defaults() {
    return _objectSpread({}, super.defaults(), {
      _model_name: 'TooltipModel',
      absolute: null,
      activator: null,
      allow_overflow: null,
      attach: null,
      bottom: null,
      close_delay: undefined,
      color: null,
      content_class: null,
      dark: null,
      disabled: null,
      eager: null,
      fixed: null,
      internal_activator: null,
      left: null,
      light: null,
      max_width: undefined,
      min_width: undefined,
      nudge_bottom: undefined,
      nudge_left: undefined,
      nudge_right: undefined,
      nudge_top: undefined,
      nudge_width: undefined,
      offset_overflow: null,
      open_delay: undefined,
      open_on_click: null,
      open_on_hover: null,
      position_x: null,
      position_y: null,
      right: null,
      tag: null,
      top: null,
      transition: null,
      value: null,
      z_index: null
    });
  }

  getVueTag() {
    // eslint-disable-line class-methods-use-this
    return 'v-tooltip';
  }

}
TooltipModel.serializers = _objectSpread({}, VuetifyWidgetModel.serializers);