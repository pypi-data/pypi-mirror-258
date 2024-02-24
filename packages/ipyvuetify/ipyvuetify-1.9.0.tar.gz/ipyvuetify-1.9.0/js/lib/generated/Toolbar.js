function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

import { VuetifyWidgetModel } from './VuetifyWidget';
export class ToolbarModel extends VuetifyWidgetModel {
  defaults() {
    return _objectSpread({}, super.defaults(), {
      _model_name: 'ToolbarModel',
      absolute: null,
      bottom: null,
      collapse: null,
      color: null,
      dark: null,
      dense: null,
      elevation: undefined,
      extended: null,
      extension_height: undefined,
      flat: null,
      floating: null,
      height: undefined,
      light: null,
      max_height: undefined,
      max_width: undefined,
      min_height: undefined,
      min_width: undefined,
      prominent: null,
      short: null,
      src: undefined,
      tag: null,
      tile: null,
      width: undefined
    });
  }

  getVueTag() {
    // eslint-disable-line class-methods-use-this
    return 'v-toolbar';
  }

}
ToolbarModel.serializers = _objectSpread({}, VuetifyWidgetModel.serializers);