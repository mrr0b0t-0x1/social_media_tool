const { app, BrowserWindow } = require('electron')
const path = require('path')
const { PythonShell } = require('python-shell')

// Only for python logging
function log_msg(args) {
    const options = {
        mode: 'json',
        pythonPath: path.resolve(__dirname, '..', '..', 'venv1', 'bin', 'python'),
        pythonOptions: ['-u'], // get print results in real-time
        scriptPath: path.resolve(__dirname, '..', '..', 'scripts'),
        args: args
    };

    const pyshell = new PythonShell('logging_init.py', options);

    pyshell.end(function (err) {
        if (err) throw err;
    })
}

function createWindow () {
  const win = new BrowserWindow({
    width: 1240,
    height: 768,
    minWidth: 1240,
    minHeight: 768,
    webPreferences: {
      // preload: path.join(__dirname, 'preload.js')
      nodeIntegration: true,
      contextIsolation: false
    }
  })

  win.loadFile(path.join(__dirname, '..', 'index.html'))
}

app.whenReady().then(() => {
  createWindow()
  // Start logging
  log_msg('--start')

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
      // Start logging
      log_msg('--start')
    }
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    // Stop logging
    log_msg('--stop')

    app.quit()
  }
})