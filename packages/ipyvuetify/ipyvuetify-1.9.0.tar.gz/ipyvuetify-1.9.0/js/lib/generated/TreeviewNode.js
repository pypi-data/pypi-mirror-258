function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

import { VuetifyWidgetModel } from './VuetifyWidget';
export class TreeviewNodeModel extends VuetifyWidgetModel {
  defaults() {
    return _objectSpread({}, super.defaults(), {
      _model_name: 'TreeviewNodeModel',
      activatable: null,
      active_class: null,
      color: null,
      expand_icon: null,
      indeterminate_icon: null,
      item: null,
      item_children: null,
      item_disabled: null,
      item_key: null,
      item_text: null,
      level: null,
      loading_icon: null,
      off_icon: null,
      on_icon: null,
      open_on_click: null,
      rounded: null,
      selectable: null,
      selected_color: null,
      shaped: null,
      transition: null
    });
  }

  getVueTag() {
    // eslint-disable-line class-methods-use-this
    return 'v-treeview-node';
  }

}
TreeviewNodeModel.serializers = _objectSpread({}, VuetifyWidgetModel.serializers);