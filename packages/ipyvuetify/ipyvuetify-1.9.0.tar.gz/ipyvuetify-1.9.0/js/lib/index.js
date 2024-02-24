import "typeface-roboto";
import "material-design-icons-iconfont/dist/material-design-icons.css";
import "@mdi/font/css/materialdesignicons.css";
import "./styles.css";
export { VuetifyView } from "./VuetifyView";
export * from "./generated";
export { HtmlModel } from "./Html";
export { VuetifyTemplateModel } from "./VuetifyTemplate";
export { ThemeModel, ThemeColorsModel } from "./Themes";

const _require = require("../package.json"),
      version = _require.version; // eslint-disable-line global-require


export { version };