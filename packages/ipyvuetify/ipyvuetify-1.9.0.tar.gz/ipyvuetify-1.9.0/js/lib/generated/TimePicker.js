function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

import { VuetifyWidgetModel } from './VuetifyWidget';
export class TimePickerModel extends VuetifyWidgetModel {
  defaults() {
    return _objectSpread({}, super.defaults(), {
      _model_name: 'TimePickerModel',
      allowed_hours: undefined,
      allowed_minutes: undefined,
      allowed_seconds: undefined,
      ampm_in_title: null,
      color: null,
      dark: null,
      disabled: null,
      format: null,
      full_width: null,
      header_color: null,
      landscape: null,
      light: null,
      max: null,
      min: null,
      no_title: null,
      readonly: null,
      scrollable: null,
      use_seconds: null,
      value: null,
      width: undefined
    });
  }

  getVueTag() {
    // eslint-disable-line class-methods-use-this
    return 'v-time-picker';
  }

}
TimePickerModel.serializers = _objectSpread({}, VuetifyWidgetModel.serializers);