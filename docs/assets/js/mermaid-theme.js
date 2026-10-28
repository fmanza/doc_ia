// Mermaid se sirve en local (assets/vendor/mermaid/); el tema lo usa porque window.mermaid existe.
// 1. startOnLoad:false ya: el script de Mermaid procesaría los bloques en el evento load y
//    duplicaría el render del tema (.claude/EDGE_CASES.md § Mermaid).
// 2. theme "default": Material no lo pasa y Mermaid 12 cambió el tema por defecto, lo que deja
//    los subgrafos ilegibles en modo oscuro. Zensical ya lo pasa; aquí solo se completa.
(function () {
  var mermaid = window.mermaid;
  if (!mermaid || typeof mermaid.initialize !== "function") return;
  var initialize = mermaid.initialize.bind(mermaid);
  initialize({ startOnLoad: false });
  mermaid.initialize = function (config) {
    var defaults = { theme: "default", themeVariables: { dropShadow: "none" } };
    return initialize(Object.assign(defaults, config));
  };
})();
