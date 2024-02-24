function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

import { VuetifyWidgetModel } from './VuetifyWidget';
export class ComboboxModel extends VuetifyWidgetModel {
  defaults() {
    return _objectSpread({}, super.defaults(), {
      _model_name: 'ComboboxModel',
      allow_overflow: null,
      append_icon: null,
      append_outer_icon: null,
      attach: null,
      auto_select_first: null,
      autofocus: null,
      background_color: null,
      cache_items: null,
      chips: null,
      clear_icon: null,
      clearable: null,
      color: null,
      counter: undefined,
      dark: null,
      deletable_chips: null,
      delimiters: null,
      dense: null,
      disable_lookup: null,
      disabled: null,
      eager: null,
      error: null,
      error_count: undefined,
      error_messages: undefined,
      filled: null,
      flat: null,
      full_width: null,
      height: undefined,
      hide_details: undefined,
      hide_no_data: null,
      hide_selected: null,
      hint: null,
      id: null,
      item_color: null,
      item_disabled: undefined,
      item_text: undefined,
      item_value: undefined,
      items: null,
      label: null,
      light: null,
      loader_height: undefined,
      loading: undefined,
      menu_props: undefined,
      messages: undefined,
      multiple: null,
      no_data_text: null,
      no_filter: null,
      open_on_clear: null,
      outlined: null,
      persistent_hint: null,
      placeholder: null,
      prefix: null,
      prepend_icon: null,
      prepend_inner_icon: null,
      readonly: null,
      return_object: null,
      reverse: null,
      rounded: null,
      rules: null,
      search_input: null,
      shaped: null,
      single_line: null,
      small_chips: null,
      solo: null,
      solo_inverted: null,
      success: null,
      success_messages: undefined,
      suffix: null,
      type: null,
      validate_on_blur: null,
      value: null
    });
  }

  getVueTag() {
    // eslint-disable-line class-methods-use-this
    return 'v-combobox';
  }

}
ComboboxModel.serializers = _objectSpread({}, VuetifyWidgetModel.serializers);