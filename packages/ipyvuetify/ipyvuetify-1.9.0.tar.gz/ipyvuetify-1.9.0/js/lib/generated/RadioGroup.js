function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

import { VuetifyWidgetModel } from './VuetifyWidget';
export class RadioGroupModel extends VuetifyWidgetModel {
  defaults() {
    return _objectSpread({}, super.defaults(), {
      _model_name: 'RadioGroupModel',
      active_class: null,
      append_icon: null,
      background_color: null,
      color: null,
      column: null,
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
      label: null,
      light: null,
      loading: null,
      mandatory: null,
      max: undefined,
      messages: undefined,
      multiple: null,
      name: null,
      persistent_hint: null,
      prepend_icon: null,
      readonly: null,
      row: null,
      rules: null,
      success: null,
      success_messages: undefined,
      validate_on_blur: null,
      value: null
    });
  }

  getVueTag() {
    // eslint-disable-line class-methods-use-this
    return 'v-radio-group';
  }

}
RadioGroupModel.serializers = _objectSpread({}, VuetifyWidgetModel.serializers);