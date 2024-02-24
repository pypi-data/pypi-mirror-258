function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

import { VuetifyWidgetModel } from './VuetifyWidget';
export class ChipModel extends VuetifyWidgetModel {
  defaults() {
    return _objectSpread({}, super.defaults(), {
      _model_name: 'ChipModel',
      active: null,
      active_class: null,
      append: null,
      close_: null,
      close_icon: null,
      color: null,
      dark: null,
      disabled: null,
      draggable: null,
      exact: null,
      exact_active_class: null,
      filter: null,
      filter_icon: null,
      href: undefined,
      input_value: null,
      label: null,
      large: null,
      light: null,
      link: null,
      nuxt: null,
      outlined: null,
      pill: null,
      replace: null,
      ripple: undefined,
      small: null,
      tag: null,
      target: null,
      text_color: null,
      to: undefined,
      value: null,
      x_large: null,
      x_small: null
    });
  }

  getVueTag() {
    // eslint-disable-line class-methods-use-this
    return 'v-chip';
  }

}
ChipModel.serializers = _objectSpread({}, VuetifyWidgetModel.serializers);