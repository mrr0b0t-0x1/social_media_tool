/**
 * Social Media Tool - A tool to gather information about a user from multiple social networks
 * Copyright (C) 2021  Arpan Adlakhiya, Aditya Mahakalkar, Nihal Nakade and Renuka Lakhe
 *
 * This file is part of Social Media Tool.
 *
 * Social Media Tool is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Social Media Tool is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Social Media Tool.  If not, see <https://www.gnu.org/licenses/>.
 */

const { app, BrowserWindow } = require('electron')
const os = require('os');
const path = require('path')
const { PythonShell } = require('python-shell')

// Set python-shell venv path
const scripts_path = path.resolve(__dirname, '..', '..', 'venv1', os.platform() === 'win32' ? 'Scripts' : 'bin')

// Only for python logging
function log_msg(args) {
    const options = {
        mode: 'json',
        pythonPath: path.resolve(scripts_path, 'python'),
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