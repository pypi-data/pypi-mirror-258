function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

import { VuetifyWidgetModel } from './VuetifyWidget';
export class CardModel extends VuetifyWidgetModel {
  defaults() {
    return _objectSpread({}, super.defaults(), {
      _model_name: 'CardModel',
      active_class: null,
      append: null,
      color: null,
      dark: null,
      disabled: null,
      elevation: undefined,
      exact: null,
      exact_active_class: null,
      flat: null,
      height: undefined,
      hover: null,
      href: undefined,
      img: null,
      light: null,
      link: null,
      loader_height: undefined,
      loading: undefined,
      max_height: undefined,
      max_width: undefined,
      min_height: undefined,
      min_width: undefined,
      nuxt: null,
      outlined: null,
      raised: null,
      replace: null,
      ripple: undefined,
      shaped: null,
      tag: null,
      target: null,
      tile: null,
      to: undefined,
      width: undefined
    });
  }

  getVueTag() {
    // eslint-disable-line class-methods-use-this
    return 'v-card';
  }

}
CardModel.serializers = _objectSpread({}, VuetifyWidgetModel.serializers);