function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

import { VuetifyWidgetModel } from './VuetifyWidget';
export class RowModel extends VuetifyWidgetModel {
  defaults() {
    return _objectSpread({}, super.defaults(), {
      _model_name: 'RowModel',
      align: null,
      align_content: null,
      align_content_lg: null,
      align_content_md: null,
      align_content_sm: null,
      align_content_xl: null,
      align_lg: null,
      align_md: null,
      align_sm: null,
      align_xl: null,
      dense: null,
      justify: null,
      justify_lg: null,
      justify_md: null,
      justify_sm: null,
      justify_xl: null,
      no_gutters: null,
      tag: null
    });
  }

  getVueTag() {
    // eslint-disable-line class-methods-use-this
    return 'v-row';
  }

}
RowModel.serializers = _objectSpread({}, VuetifyWidgetModel.serializers);