function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

import { VuetifyWidgetModel } from './VuetifyWidget';
export class AppBarModel extends VuetifyWidgetModel {
  defaults() {
    return _objectSpread({}, super.defaults(), {
      _model_name: 'AppBarModel',
      absolute: null,
      app: null,
      bottom: null,
      clipped_left: null,
      clipped_right: null,
      collapse: null,
      collapse_on_scroll: null,
      color: null,
      dark: null,
      dense: null,
      elevate_on_scroll: null,
      elevation: undefined,
      extended: null,
      extension_height: undefined,
      fade_img_on_scroll: null,
      fixed: null,
      flat: null,
      floating: null,
      height: undefined,
      hide_on_scroll: null,
      inverted_scroll: null,
      light: null,
      max_height: undefined,
      max_width: undefined,
      min_height: undefined,
      min_width: undefined,
      prominent: null,
      scroll_off_screen: null,
      scroll_target: null,
      scroll_threshold: undefined,
      short: null,
      shrink_on_scroll: null,
      src: undefined,
      tag: null,
      tile: null,
      value: null,
      width: undefined
    });
  }

  getVueTag() {
    // eslint-disable-line class-methods-use-this
    return 'v-app-bar';
  }

}
AppBarModel.serializers = _objectSpread({}, VuetifyWidgetModel.serializers);