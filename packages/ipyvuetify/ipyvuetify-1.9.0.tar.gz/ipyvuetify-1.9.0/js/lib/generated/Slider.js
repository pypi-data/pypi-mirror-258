function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

import { VuetifyWidgetModel } from './VuetifyWidget';
export class SliderModel extends VuetifyWidgetModel {
  defaults() {
    return _objectSpread({}, super.defaults(), {
      _model_name: 'SliderModel',
      append_icon: null,
      background_color: null,
      color: null,
      dark: null,
      dense: null,
      disabled: null,
      error: null,
      error_count: undefined,
      error_messages: undefined,
      height: undefined,
      hide_details: undefined,
      hint: null,
      id: null,
      inverse_label: null,
      label: null,
      light: null,
      loader_height: undefined,
      loading: undefined,
      max: undefined,
      messages: undefined,
      min: undefined,
      persistent_hint: null,
      prepend_icon: null,
      readonly: null,
      rules: null,
      step: undefined,
      success: null,
      success_messages: undefined,
      thumb_color: null,
      thumb_label: undefined,
      thumb_size: undefined,
      tick_labels: null,
      tick_size: undefined,
      ticks: undefined,
      track_color: null,
      track_fill_color: null,
      validate_on_blur: null,
      value: null,
      vertical: null
    });
  }

  getVueTag() {
    // eslint-disable-line class-methods-use-this
    return 'v-slider';
  }

}
SliderModel.serializers = _objectSpread({}, VuetifyWidgetModel.serializers);