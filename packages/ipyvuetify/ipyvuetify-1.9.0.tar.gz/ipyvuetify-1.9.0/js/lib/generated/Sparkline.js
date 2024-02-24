function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

import { VuetifyWidgetModel } from './VuetifyWidget';
export class SparklineModel extends VuetifyWidgetModel {
  defaults() {
    return _objectSpread({}, super.defaults(), {
      _model_name: 'SparklineModel',
      auto_draw: null,
      auto_draw_duration: null,
      auto_draw_easing: null,
      auto_line_width: null,
      color: null,
      fill: null,
      gradient: null,
      gradient_direction: null,
      height: undefined,
      label_size: undefined,
      labels: null,
      line_width: undefined,
      padding: undefined,
      show_labels: null,
      smooth: undefined,
      type: null,
      value: null,
      width: undefined
    });
  }

  getVueTag() {
    // eslint-disable-line class-methods-use-this
    return 'v-sparkline';
  }

}
SparklineModel.serializers = _objectSpread({}, VuetifyWidgetModel.serializers);