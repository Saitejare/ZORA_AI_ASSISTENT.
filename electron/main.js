const {
  app,
  BrowserWindow,
  shell,
} = require("electron");

const path = require("path");
const fs = require("fs");
const { spawn } = require("child_process");

let mainWindow = null;
let backendProcess = null;

const BACKEND_HOST = "127.0.0.1";
const BACKEND_PORT = 8000;

const gotTheLock = app.requestSingleInstanceLock();

if (!gotTheLock) {
  app.quit();
} else {
  app.on("second-instance", () => {
    if (!mainWindow) {
      return;
    }

    if (mainWindow.isMinimized()) {
      mainWindow.restore();
    }

    mainWindow.show();
    mainWindow.focus();
    mainWindow.moveTop();
  });
}

/* =========================================================
   PATHS
   ========================================================= */

const PROJECT_ROOT = path.join(
  __dirname,
  ".."
);


/*
 * DEVELOPMENT
 *
 * Project:
 *
 * AI-Assistant/
 * ├── electron/
 * ├── frontend/
 * ├── backend/
 * └── dist/
 *      └── ZORA-backend.exe
 *
 *
 * PRODUCTION
 *
 * Installed application:
 *
 * resources/
 * ├── backend/
 * │    ├── ZORA-backend.exe
 * │    └── .env
 * │
 * └── frontend/
 *      └── dist/
 *
 */


/* =========================================================
   FRONTEND PATH
   ========================================================= */


function getFrontendPath() {

  return path.join(
    app.getAppPath(),
    "frontend",
    "dist",
    "index.html"
  );

}


/* =========================================================
   BACKEND PATH
   ========================================================= */

function getBackendExecutable() {

  if (app.isPackaged) {

    return path.join(
      process.resourcesPath,
      "backend",
      "ZORA-backend.exe"
    );

  }

  return path.join(
    PROJECT_ROOT,
    "dist",
    "ZORA-backend.exe"
  );
}


/* =========================================================
   LOG
   ========================================================= */

function log(message) {

  console.log(
    `[ZORA] ${message}`
  );

}


/* =========================================================
   DELAY
   ========================================================= */

function delay(ms) {

  return new Promise(
    (resolve) => {

      setTimeout(
        resolve,
        ms
      );

    }
  );

}


/* =========================================================
   START BACKEND
   ========================================================= */

function startBackend() {

  if (backendProcess) {

    log(
      "Backend process already exists."
    );

    return;
  }


  const backendExecutable =
    getBackendExecutable();


  if (
    !fs.existsSync(
      backendExecutable
    )
  ) {

    throw new Error(
      `ZORA backend executable not found:\n${backendExecutable}`
    );

  }


  const backendDirectory =
    path.dirname(
      backendExecutable
    );


  log(
    `Backend executable: ${backendExecutable}`
  );

  log(
    `Backend directory: ${backendDirectory}`
  );


  backendProcess =
    spawn(
      backendExecutable,
      [],
      {
        cwd: backendDirectory,

        windowsHide: true,

        stdio: [
          "ignore",
          "pipe",
          "pipe",
        ],
      }
    );


  backendProcess.stdout.on(
    "data",
    (data) => {

      process.stdout.write(
        `[ZORA BACKEND] ${data}`
      );

    }
  );


  backendProcess.stderr.on(
    "data",
    (data) => {

      process.stderr.write(
        `[ZORA BACKEND] ${data}`
      );

    }
  );


  backendProcess.on(
    "error",
    (error) => {

      console.error(
        "[ZORA] Backend process error:",
        error
      );

    }
  );


  backendProcess.on(
    "exit",
    (
      code,
      signal
    ) => {

      log(
        `ZORA backend exited. code=${code} signal=${signal}`
      );

      backendProcess = null;

    }
  );

}


/* =========================================================
   WAIT FOR HTTP BACKEND
   ========================================================= */

async function waitForBackend(
  timeout = 120000
) {

  const startTime =
    Date.now();


  log(
    "Waiting for ZORA backend..."
  );


  while (
    Date.now() -
      startTime <
    timeout
  ) {

    try {

      const response =
        await fetch(
          `http://${BACKEND_HOST}:${BACKEND_PORT}/health`
        );


      if (
        response.ok
      ) {

        log(
          "ZORA backend is online."
        );

        return true;

      }

    } catch (error) {

      // Backend is still starting.
      // Keep waiting until the startup timeout.

    }


    await delay(
      1000
    );

  }


  throw new Error(
    "ZORA backend did not become available within 120 seconds."
  );

}


/* =========================================================
   INITIALIZE MICROPHONE
   ========================================================= */

async function initializeMicrophone() {

  log(
    "Initializing ZORA microphone..."
  );


  try {

    const response =
      await fetch(
        `http://${BACKEND_HOST}:${BACKEND_PORT}/microphone/initialize`,
        {
          method:
            "POST",

          headers: {
            "Content-Type":
              "application/json",
          },

          body:
            JSON.stringify({}),
        }
      );


    if (
      !response.ok
    ) {

      const text =
        await response
          .text()
          .catch(
            () => ""
          );


      throw new Error(
        `Microphone initialization failed (${response.status}) ${text}`
      );

    }


    const result =
      await response.json();


    if (
      result?.data?.microphone !== true
    ) {

      throw new Error(
        "Backend did not confirm microphone readiness."
      );

    }


    log(
      "ZORA microphone initialized."
    );


    return true;

  } catch (error) {

    console.error(
      "[ZORA] Microphone initialization error:",
      error
    );

    throw error;

  }

}


/* =========================================================
   WAIT FOR ZORA READY
   ========================================================= */

async function waitForZoraReady(
  timeout = 120000
) {

  const startTime =
    Date.now();


  log(
    "Waiting for complete ZORA initialization..."
  );


  while (
    Date.now() -
      startTime <
    timeout
  ) {

    try {

      const response =
        await fetch(
          `http://${BACKEND_HOST}:${BACKEND_PORT}/ready`
        );


      if (
        response.ok
      ) {

        const result =
          await response.json();


        if (
          result?.data?.ready === true
        ) {

          log(
            "ZORA is completely ready."
          );

          return true;

        }

      }

    } catch (_) {

      // Backend is still becoming ready.

    }


    await delay(
      1000
    );

  }


  throw new Error(
    "ZORA did not become fully ready within 120 seconds."
  );

}


/* =========================================================
   CREATE WINDOW
   ========================================================= */

function createWindow() {

  const indexFile =
    getFrontendPath();


  if (
    !fs.existsSync(
      indexFile
    )
  ) {

    throw new Error(
      `Frontend index.html not found:\n${indexFile}`
    );

  }


  log(
    `Frontend: ${indexFile}`
  );


    mainWindow = new BrowserWindow({
    width: 1440,
    height: 900,
    minWidth: 1000,
    minHeight: 700,
    backgroundColor: "#020617",
    show: false,
    autoHideMenuBar: true,
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
    },
  });

  mainWindow.once("ready-to-show", () => {
    if (!mainWindow) {
      return;
    }

    mainWindow.show();
    mainWindow.focus();
    mainWindow.moveTop();

    log("ZORA interface displayed.");
  });

  mainWindow.loadFile(indexFile);

  mainWindow.webContents.setWindowOpenHandler(
    ({ url }) => {

      shell.openExternal(
        url
      );


      return {
        action:
          "deny",
      };

    }
  );


  mainWindow.webContents.on(
    "did-fail-load",
    (
      event,
      errorCode,
      errorDescription
    ) => {

      console.error(
        "[ZORA] Frontend failed to load:",
        errorCode,
        errorDescription
      );

    }
  );


  mainWindow.webContents.on(
    "did-finish-load",
    () => {

      log(
        "Frontend loaded successfully."
      );

    }
  );


  mainWindow.on(
    "closed",
    () => {

      mainWindow =
        null;

    }
  );

}


/* =========================================================
   START ZORA
   ========================================================= */

async function startZora() {

  try {

    /*
     * STEP 1
     *
     * Start packaged backend EXE
     */

    startBackend();


    /*
     * STEP 2
     *
     * Wait for FastAPI
     */

    await waitForBackend();


    /*
     * STEP 3
     *
     * Initialize microphone
     */

    await initializeMicrophone();


    /*
     * STEP 4
     *
     * Wait for complete ZORA initialization
     */

    await waitForZoraReady();


    /*
     * STEP 5
     *
     * Open frontend
     */

    createWindow();


    log(
      "ZORA startup sequence completed."
    );

  } catch (error) {

    console.error(
      "[ZORA] Startup failed:",
      error
    );


    stopBackend();


    app.quit();

  }

}


/* =========================================================
   STOP BACKEND
   ========================================================= */

function stopBackend() {

  if (
    !backendProcess
  ) {

    return;

  }


  log(
    "Stopping ZORA backend..."
  );


  const processToStop =
    backendProcess;


  backendProcess =
    null;


  try {

    if (
      process.platform ===
      "win32"
    ) {

      spawn(
        "taskkill",
        [
          "/pid",
          String(
            processToStop.pid
          ),
          "/T",
          "/F",
        ],
        {
          windowsHide:
            true,
        }
      );

    } else {

      processToStop.kill(
        "SIGTERM"
      );

    }

  } catch (error) {

    console.error(
      "[ZORA] Failed to stop backend:",
      error
    );

  }

}


/* =========================================================
   ELECTRON READY
   ========================================================= */

app.whenReady().then(
  () => {

    void startZora();


    app.on("activate", () => {
  if (mainWindow) {
    if (mainWindow.isMinimized()) {
      mainWindow.restore();
    }

    mainWindow.show();
    mainWindow.focus();
    mainWindow.moveTop();

    return;
  }

  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

  }
);


/* =========================================================
   BEFORE QUIT
   ========================================================= */

app.on(
  "before-quit",
  () => {

    stopBackend();

  }
);


/* =========================================================
   ALL WINDOWS CLOSED
   ========================================================= */

app.on(
  "window-all-closed",
  () => {

    if (
      process.platform !==
      "darwin"
    ) {

      app.quit();

    }

  }
);