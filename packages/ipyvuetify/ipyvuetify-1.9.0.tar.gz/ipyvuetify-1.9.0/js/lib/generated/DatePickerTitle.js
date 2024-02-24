function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

import { VuetifyWidgetModel } from './VuetifyWidget';
export class DatePickerTitleModel extends VuetifyWidgetModel {
  defaults() {
    return _objectSpread({}, super.defaults(), {
      _model_name: 'DatePickerTitleModel',
      color: null,
      date: null,
      disabled: null,
      readonly: null,
      selecting_year: null,
      value: null,
      year: undefined,
      year_icon: null
    });
  }

  getVueTag() {
    // eslint-disable-line class-methods-use-this
    return 'v-date-picker-title';
  }

}
DatePickerTitleModel.serializers = _objectSpread({}, VuetifyWidgetModel.serializers);