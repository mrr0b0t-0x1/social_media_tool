// const electron = require("electron");
// const app = electron.app;
// const BrowserWindow = electron.BrowserWindow;
// //const {app, BrowserWindow} = require('electron')
// const path = require('path')
// const url = require('url')
//
//
// let win;
//
// function createWindow () {
//
//   win = new BrowserWindow({
//     webPreferences: {
//       nodeIntegration: true,
//       contextIsolation: false,
//     },
//     width: 1240,
//     height: 768,
//     minWidth: 1240,
//     minHeight: 768
//   })
//
//   win.loadURL(url.format({
//     pathname: path.join(__dirname, '../index.html'),
//     protocol: 'file:',
//     slashes: true
//   }));
//
//
//   win.on('closed', () => {
//     win = null
//   });
// }
//
// app.on('ready', createWindow);
//
//
// app.on('window-all-closed', () => {
//   if (process.platform !== 'darwin') {
//     app.quit();
//   }
// });
//
// app.on('activate', () => {
//   if (win === null) {
//     createWindow();
//   }
// });

const { app, BrowserWindow } = require('electron')
const path = require('path')

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

  win.loadFile(path.join(__dirname, '../index.html'))
}

app.whenReady().then(() => {
  createWindow()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})