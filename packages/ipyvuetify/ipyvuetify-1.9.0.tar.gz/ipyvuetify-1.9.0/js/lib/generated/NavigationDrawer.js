function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

import { VuetifyWidgetModel } from './VuetifyWidget';
export class NavigationDrawerModel extends VuetifyWidgetModel {
  defaults() {
    return _objectSpread({}, super.defaults(), {
      _model_name: 'NavigationDrawerModel',
      absolute: null,
      app: null,
      bottom: null,
      clipped: null,
      color: null,
      dark: null,
      disable_resize_watcher: null,
      disable_route_watcher: null,
      expand_on_hover: null,
      fixed: null,
      floating: null,
      height: undefined,
      hide_overlay: null,
      light: null,
      mini_variant: null,
      mini_variant_width: undefined,
      mobile_break_point: undefined,
      overlay_color: null,
      overlay_opacity: undefined,
      permanent: null,
      right: null,
      src: undefined,
      stateless: null,
      tag: null,
      temporary: null,
      touchless: null,
      value: null,
      width: undefined
    });
  }

  getVueTag() {
    // eslint-disable-line class-methods-use-this
    return 'v-navigation-drawer';
  }

}
NavigationDrawerModel.serializers = _objectSpread({}, VuetifyWidgetModel.serializers);