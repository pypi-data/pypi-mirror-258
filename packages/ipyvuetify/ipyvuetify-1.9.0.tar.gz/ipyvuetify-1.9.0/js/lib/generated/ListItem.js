function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

import { VuetifyWidgetModel } from './VuetifyWidget';
export class ListItemModel extends VuetifyWidgetModel {
  defaults() {
    return _objectSpread({}, super.defaults(), {
      _model_name: 'ListItemModel',
      active_class: null,
      append: null,
      color: null,
      dark: null,
      dense: null,
      disabled: null,
      exact: null,
      exact_active_class: null,
      href: undefined,
      inactive: null,
      input_value: null,
      light: null,
      link: null,
      nuxt: null,
      replace: null,
      ripple: undefined,
      selectable: null,
      tag: null,
      target: null,
      three_line: null,
      to: undefined,
      two_line: null,
      value: null
    });
  }

  getVueTag() {
    // eslint-disable-line class-methods-use-this
    return 'v-list-item';
  }

}
ListItemModel.serializers = _objectSpread({}, VuetifyWidgetModel.serializers);