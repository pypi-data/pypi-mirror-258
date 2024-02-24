function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

import { VuetifyWidgetModel } from './VuetifyWidget';
export class CheckboxModel extends VuetifyWidgetModel {
  defaults() {
    return _objectSpread({}, super.defaults(), {
      _model_name: 'CheckboxModel',
      append_icon: null,
      background_color: null,
      color: null,
      dark: null,
      dense: null,
      disabled: null,
      error: null,
      error_count: undefined,
      error_messages: undefined,
      false_value: null,
      height: undefined,
      hide_details: undefined,
      hint: null,
      id: null,
      indeterminate: null,
      indeterminate_icon: null,
      input_value: null,
      label: null,
      light: null,
      loading: null,
      messages: undefined,
      multiple: null,
      off_icon: null,
      on_icon: null,
      persistent_hint: null,
      prepend_icon: null,
      readonly: null,
      ripple: undefined,
      rules: null,
      success: null,
      success_messages: undefined,
      true_value: null,
      validate_on_blur: null,
      value: null
    });
  }

  getVueTag() {
    // eslint-disable-line class-methods-use-this
    return 'v-checkbox';
  }

}
CheckboxModel.serializers = _objectSpread({}, VuetifyWidgetModel.serializers);