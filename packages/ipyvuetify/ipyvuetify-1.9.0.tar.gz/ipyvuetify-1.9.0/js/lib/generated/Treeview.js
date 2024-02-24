function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

import { VuetifyWidgetModel } from './VuetifyWidget';
export class TreeviewModel extends VuetifyWidgetModel {
  defaults() {
    return _objectSpread({}, super.defaults(), {
      _model_name: 'TreeviewModel',
      activatable: null,
      active: null,
      active_class: null,
      color: null,
      dark: null,
      dense: null,
      expand_icon: null,
      hoverable: null,
      indeterminate_icon: null,
      item_children: null,
      item_disabled: null,
      item_key: null,
      item_text: null,
      items: null,
      light: null,
      loading_icon: null,
      multiple_active: null,
      off_icon: null,
      on_icon: null,
      open_: null,
      open_all: null,
      open_on_click: null,
      return_object: null,
      rounded: null,
      search: null,
      selectable: null,
      selected_color: null,
      selection_type: null,
      shaped: null,
      transition: null,
      value: null
    });
  }

  getVueTag() {
    // eslint-disable-line class-methods-use-this
    return 'v-treeview';
  }

}
TreeviewModel.serializers = _objectSpread({}, VuetifyWidgetModel.serializers);