const {
  app,
  BrowserWindow,
  Menu,
  dialog
} = require('electron');
const path = require("path");
const url = require("url");

let win;
// let subpy = null;

function createWindow() {
  // Creating the browser window
  win = new BrowserWindow({
    width: 800,
    height: 600,
    backgroundColor: 'white',
    title: 'eKTAB',
    icon: path.join(__dirname, 'api/dist/ktab-electron/assets/images/icon.png')
  });

  win.loadURL(
    url.format({
      pathname: path.join(__dirname, 'api/dist/ktab-electron/index.html'),
      protocol: "file:",
      slashes: true
    })
  );

  win.webContents.openDevTools()

  // Window close
  win.on('close', function () {
    win = null
  });
}

// Create window on app initilization
app.on('ready', function () {
    // subpy = require('child_process').spawn('python', [__dirname + '/api/run_app.py']);
    createWindow();
    const template = [{
        label: 'Edit',
        submenu: [{
            role: 'undo'
            },
            {
                label: 'Open SQLite File',
                click: () => {
                    let filenames = dialog.showOpenDialog({
                        properties: ["openFile"],
                        filters: [
                        {name: "SQLite", extensions: ["db", "sqlite"]}
                        ]}
                    );
                    console.log(`Opening file from menu: ${filenames[0]}`);
                }
            },
            {
            role: 'redo'
            },
            {
            type: 'separator'
            },
            {
            role: 'cut'
            },
            {
            role: 'copy'
            },
            {
            role: 'paste'
            },
            {
            role: 'pasteandmatchstyle'
            },
            {
            role: 'delete'
            },
            {
            role: 'selectall'
            }
        ]
        },
        {
        label: 'View',
        submenu: [{
            role: 'reload'
            },
            {
            role: 'forcereload'
            },
            {
            role: 'toggledevtools'
            },
            {
            type: 'separator'
            },
            {
            role: 'resetzoom'
            },
            {
            role: 'zoomin'
            },
            {
            role: 'zoomout'
            },
            {
            type: 'separator'
            },
            {
            role: 'togglefullscreen'
            }
        ]
        },
        {
        role: 'window',
        submenu: [{
            role: 'minimize'
            },
            {
            role: 'close'
            }
        ]
        },
        {
        role: 'help',
        submenu: [{
            label: 'Learn More',
            click() {
            require('electron').shell.openExternal('https://ktab.software')
            }
        }]
        }
    ]

    if (process.platform === 'darwin') {
        console.log()
        template.unshift({
        label: app.getName(),
        submenu: [{
            role: 'about'
            },
            {
            type: 'separator'
            },
            {
            role: 'services'
            },
            {
            type: 'separator'
            },
            {
            role: 'hide'
            },
            {
            role: 'hideothers'
            },
            {
            role: 'unhide'
            },
            {
            type: 'separator'
            },
            {
            role: 'quit'
            }
        ]
        })

        // Edit menu
        template[1].submenu.push({
        type: 'separator'
        }, {
        label: 'Speech',
        submenu: [{
            role: 'startspeaking'
            },
            {
            role: 'stopspeaking'
            }
        ]
        })

        // Window menu
        template[3].submenu = [{
            role: 'close'
        },
        {
            role: 'minimize'
        },
        {
            role: 'zoom'
        },
        {
            type: 'separator'
        },
        {
            role: 'front'
        }
        ]
    }
    const menu = Menu.buildFromTemplate(template)
    Menu.setApplicationMenu(menu)
});

// Quit all app windows upon exit
app.on('window-all-closed', function () {
  // On macOs
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', function () {
  // macOs specific close all process
  if (win == null) {
    createWindow();
  }
});

let pyProc = null

const createPyProc = () => {
  let script = path.join(__dirname, 'api', 'run_app.py')
  let pythonPath = path.join(__dirname, 'venv', 'bin', 'python')
  console.log(__dirname)
  pyProc = require('child_process').spawn(__dirname + '/venv/bin/python', [__dirname + '/api/run_app.py', 'start']);
  if (pyProc != null) {
    console.log('child process success')
  }
}

const exitPyProc = () => {
  pyProc.kill()
  pyProc = null
}

app.on('ready', createPyProc)
app.on('will-quit', exitPyProc)