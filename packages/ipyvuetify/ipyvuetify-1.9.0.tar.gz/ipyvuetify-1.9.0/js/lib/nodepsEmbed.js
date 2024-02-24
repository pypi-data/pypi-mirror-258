import "./styles.css";
export { VuetifyView } from "./VuetifyView";
export * from "./generated";
export { HtmlModel } from "./Html";
export { VuetifyTemplateModel } from "./VuetifyTemplate";
export { ThemeModel, ThemeColorsModel } from "./Themes";

const _require = require("../package.json"),
      version = _require.version; // eslint-disable-line global-require


export { version };