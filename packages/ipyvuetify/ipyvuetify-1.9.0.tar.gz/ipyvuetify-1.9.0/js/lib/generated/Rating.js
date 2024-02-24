function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

import { VuetifyWidgetModel } from './VuetifyWidget';
export class RatingModel extends VuetifyWidgetModel {
  defaults() {
    return _objectSpread({}, super.defaults(), {
      _model_name: 'RatingModel',
      background_color: null,
      clearable: null,
      close_delay: undefined,
      color: null,
      dark: null,
      dense: null,
      empty_icon: null,
      full_icon: null,
      half_icon: null,
      half_increments: null,
      hover: null,
      large: null,
      length: undefined,
      light: null,
      open_delay: undefined,
      readonly: null,
      ripple: undefined,
      size: undefined,
      small: null,
      value: null,
      x_large: null,
      x_small: null
    });
  }

  getVueTag() {
    // eslint-disable-line class-methods-use-this
    return 'v-rating';
  }

}
RatingModel.serializers = _objectSpread({}, VuetifyWidgetModel.serializers);