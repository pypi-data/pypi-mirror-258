function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

import { VuetifyWidgetModel } from './VuetifyWidget';
export class DatePickerModel extends VuetifyWidgetModel {
  defaults() {
    return _objectSpread({}, super.defaults(), {
      _model_name: 'DatePickerModel',
      color: null,
      dark: null,
      disabled: null,
      event_color: undefined,
      events: undefined,
      first_day_of_week: undefined,
      full_width: null,
      header_color: null,
      landscape: null,
      light: null,
      locale: null,
      locale_first_day_of_year: undefined,
      max: null,
      min: null,
      multiple: null,
      next_icon: null,
      no_title: null,
      picker_date: null,
      prev_icon: null,
      range: null,
      reactive: null,
      readonly: null,
      scrollable: null,
      selected_items_text: null,
      show_current: undefined,
      show_week: null,
      type: null,
      value: undefined,
      width: undefined,
      year_icon: null
    });
  }

  getVueTag() {
    // eslint-disable-line class-methods-use-this
    return 'v-date-picker';
  }

}
DatePickerModel.serializers = _objectSpread({}, VuetifyWidgetModel.serializers);