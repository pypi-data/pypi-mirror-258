function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

import { VuetifyWidgetModel } from './VuetifyWidget';
export class DatePickerMonthTableModel extends VuetifyWidgetModel {
  defaults() {
    return _objectSpread({}, super.defaults(), {
      _model_name: 'DatePickerMonthTableModel',
      color: null,
      current: null,
      dark: null,
      disabled: null,
      event_color: undefined,
      events: undefined,
      light: null,
      locale: null,
      max: null,
      min: null,
      range: null,
      readonly: null,
      scrollable: null,
      table_date: null,
      value: undefined
    });
  }

  getVueTag() {
    // eslint-disable-line class-methods-use-this
    return 'v-date-picker-month-table';
  }

}
DatePickerMonthTableModel.serializers = _objectSpread({}, VuetifyWidgetModel.serializers);