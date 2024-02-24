function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

import { VuetifyWidgetModel } from './VuetifyWidget';
export class CalendarDailyModel extends VuetifyWidgetModel {
  defaults() {
    return _objectSpread({}, super.defaults(), {
      _model_name: 'CalendarDailyModel',
      color: null,
      dark: null,
      end: null,
      first_interval: undefined,
      hide_header: null,
      interval_count: undefined,
      interval_height: undefined,
      interval_minutes: undefined,
      interval_width: undefined,
      light: null,
      locale: null,
      max_days: null,
      now: null,
      short_intervals: null,
      short_weekdays: null,
      start: null,
      weekdays: undefined
    });
  }

  getVueTag() {
    // eslint-disable-line class-methods-use-this
    return 'v-calendar-daily';
  }

}
CalendarDailyModel.serializers = _objectSpread({}, VuetifyWidgetModel.serializers);