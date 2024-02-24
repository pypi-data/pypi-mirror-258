function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

/* eslint camelcase: off */
import { VueTemplateModel } from "jupyter-vue";
export class VuetifyTemplateModel extends VueTemplateModel {
  defaults() {
    return _objectSpread({}, super.defaults(), {
      _model_name: "VuetifyTemplateModel",
      _view_name: "VuetifyView",
      _view_module: "jupyter-vuetify",
      _model_module: "jupyter-vuetify",
      _view_module_version: "0.1.0",
      _model_module_version: "0.1.0"
    });
  }

}
VuetifyTemplateModel.serializers = _objectSpread({}, VueTemplateModel.serializers);