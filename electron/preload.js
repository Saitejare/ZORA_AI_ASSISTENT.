const {
  contextBridge,
  ipcRenderer,
} = require("electron");


contextBridge.exposeInMainWorld(
  "zoraDesktop",
  {

    getBackendUrl:
      () =>
        ipcRenderer.invoke(
          "zora:get-backend-url",
        ),

    minimize:
      () =>
        ipcRenderer.invoke(
          "zora:minimize",
        ),

    maximize:
      () =>
        ipcRenderer.invoke(
          "zora:maximize",
        ),

    close:
      () =>
        ipcRenderer.invoke(
          "zora:close",
        ),

    show:
      () =>
        ipcRenderer.invoke(
          "zora:show",
        ),

    openExternal:
      (url) =>
        ipcRenderer.invoke(
          "zora:open-external",
          url,
        ),
  },
);