const fs = require('fs');
const { PythonShell } = require('python-shell')

const liveResults = document.getElementById('liveResults');

let username;

const siteList = [
    'facebook',
    'instagram',
    'twitter',
    'reddit',
    'linkedin'
];

const tabAndPanes = {
    'facebook': [
        document.getElementById('list-facebook-list'),
        document.getElementById('list-facebook')
    ],
    'instagram': [
        document.getElementById('list-instagram-list'),
        document.getElementById('list-instagram')
    ],
    'twitter': [
        document.getElementById('list-twitter-list'),
        document.getElementById('list-twitter')
    ],
    'reddit': [
        document.getElementById('list-reddit-list'),
        document.getElementById('list-reddit')
    ],
    'linkedin': [
        document.getElementById('list-linkedin-list'),
        document.getElementById('list-linkedin')
    ]
};

// function traverseDataTree(obj, site) {
//     Object.keys(obj).forEach(function (key) {
//         // console.log(key);
//         if (obj[key] !== null && obj[key].length !== 0) {
//             if (typeof obj[key] === 'object') {
//                 tabAndPanes[site][1].innerHTML += key + ": <br />";
//                 if (Array.isArray( obj[key] )) {
//                     // for (const val of obj[key])
//                         // traverseDataTree(val, site);
//                         tabAndPanes[site][1].innerHTML += obj[key].join(", ") + "<br />";
//                 }
//                 else {
//                     traverseDataTree(obj[key], site);
//                 }
//             }
//             else {
//                 tabAndPanes[site][1].innerHTML += key + ": " + obj[key] + "<br />";
//                 // console.log(nestKey + " -> " + key + ": " + obj[key]);
//                 // let txt = document.createElement("span");
//                 // txt.innerText = key + ": " + obj[key]
//                 // txt.innerHTML += "<br />"
//                 // parent.appendChild(txt);
//             }
//         }
//     });
// }
function getCreateSection(section) {
    let sectionName = "list" + section.split(username)[1];
    if (sectionName.includes("fb")) {
        sectionName = sectionName.substring(0, sectionName.lastIndexOf("-"));
    }

    const sectionElement = document.getElementById(sectionName);

    // if (!sectionElement.firstElementChild) {
    //     sectionElement.innerHTML =  '<div id="' + sectionName + '" class="row h-100">' +
    //                                 '   <div class="col-12">' +
    //                                 '       <table class="table table-striped">' +
    //                                 '       </table>' +
    //                                 '   </div>' +
    //                                 '</div>';
    // }

    return sectionElement;
}

function generateID(length) {
    let result = [];
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const charactersLength = characters.length;
    for ( let i = 0; i < length; i++ ) {
        result.push( characters.charAt( Math.floor(Math.random() * charactersLength) ) );
    }
   return result.join('');
}

function createTableElement(element) {
    const id = generateID(6);

    element =   '<table id="' + id + '" class="table">' +
                '   <tr></tr>' +
                '</table>';

    return element;
}

function JSONToHTMLTable(data, sectionElement) {
    const options = {
        mode: 'json',
        pythonPath: '../venv1/bin/python',
        pythonOptions: ['-u'], // get print results in real-time
        scriptPath: '../scripts',
        args: ['--json-to-html', JSON.stringify(data)]
    };

    let response = null;

    // PythonShell.run('main.py', options, function (err, results) {
    //     if (err) throw err;
    //     return results;
    //     // if (results[0]['ERROR']) {
    //     //     liveResults.firstElementChild.innerHTML += "<span class='d-block'><span class='text-grey'>❯</span>" +
    //     //         "&emsp;<span class='text-danger'>Error: " + results[0]['ERROR'] + "</span></span>"
    //     //     console.log("Error: " + results[0]['ERROR']);
    //     // }
    //     // else if (results[0]['DATA']) {
    //     //     response = results[0]['DATA'];
    //     // }
    // });


    // return response;

    const pyshell = new PythonShell('main.py', options);

    pyshell.on('message', function (message) {
        if (message.ERROR) {
            liveResults.firstElementChild.innerHTML += "<span class='d-block'><span class='text-grey'>❯</span>" +
                "&emsp;<span class='text-danger'>Error: " + message.ERROR + "</span></span>"
            console.log("Error: " + message.ERROR);
        }
        else if (message.DATA) {
            sectionElement.innerHTML = message.DATA;
        }
    });


}

function traverseDataTree(obj, site, section, table, key=null) {
    const sectionElement = getCreateSection(section);
    JSONToHTMLTable(obj, sectionElement);

    // console.log(sectionElement);

    // sectionElement.querySelector(".col-12").innerHTML = JSONToHTMLTable(obj);

    // if (!table)
    //     table = sectionElement.querySelector(".table.table-striped");
    //
    // if (typeof obj === 'object') {
    //     if (Array.isArray(obj)) {
    //         for (const [idx, val] of obj.entries()) {
    //             if (typeof val === 'object') {
    //                 traverseDataTree(val, site, section, table);
    //             }
    //             else {
    //                 // console.log('inside array if else');
    //                 // if (idx !== obj.length - 1) {
    //                 //     sectionElement.querySelector(".col-12").innerHTML += val + ", ";
    //                 // }
    //                 // else {
    //                 //     sectionElement.querySelector(".col-12").innerHTML += val + "<br />";
    //                 // }
    //                 if (!table.firstElementChild)
    //                     table.innerHTML += '<tr></tr>';
    //                 else
    //                     table.firstElementChild.innerHTML += '<td>' + val + '</td>';
    //             }
    //         }
    //     }
    //     else {
    //         Object.keys(obj).forEach( function (key) {
    //             if (obj[key] !== null && obj[key].length !== 0) {
    //                 if (typeof obj[key] === 'object') {
    //                     // sectionElement.querySelector(".col-12").innerHTML += key + ": <br />";
    //                     let childTable = createTableElement();
    //                     table.innerHTML +=  '<tr>' +
    //                                         '   <td>' + key + '</td>' +
    //                                         '   <td>' + childTable + '</td>' +
    //                                         '</tr>';
    //                     traverseDataTree(obj[key], site, section, childTable);
    //                 }
    //                 else
    //                     traverseDataTree(obj[key], site, section, table, key);
    //             }
    //         })
    //     }
    // } else {
    //     if (key)
    //         // sectionElement.querySelector(".col-12").innerHTML += key + ": " + obj + "<br />";
    //         table.innerHTML +=  '<tr>' +
    //                             '   <td>' + key + '</td>' +
    //                             '   <td>' + obj + '</td>' +
    //                             '</tr>';
    // }
}

function readJSONFile(path, callback) {
    try {
        const data = fs.readFileSync(path);
        const dataJSON = JSON.parse(data.toString());
        return callback && callback(null, dataJSON);
    } catch (err) {
        return callback && callback(err);
    }
}

function traverseDBTree(obj, site) {
    Object.keys(obj).forEach(function (key) {
        if (obj[key] !== null) {
            if (obj[key] !== null && typeof obj[key] === 'object')
                traverseDBTree(obj[key], site);
            else {
                if (obj[key].split('.').pop() === 'json') {
                    readJSONFile(obj[key], (err, data) => {
                        if (err) {
                            console.log(err);
                        } else {
                            traverseDataTree(data, site, key, null);
                        }
                    });
                }
            }
        }
    });
}

function parseDBData(uname, obj) {
    username = uname;

    Object.keys(obj['sites_found']).forEach(function (site) {
        if (siteList.includes(site)) {
            // show those tabs whose sites are found
            $(tabAndPanes[site][0]).removeClass('d-none');
            $(tabAndPanes[site][1]).removeClass('d-none');

            traverseDBTree(obj['sites_found'][site], site);
        }
    });
}

module.exports = {
    parseDBData: parseDBData,
    siteList: siteList,
    tabAndPanes: tabAndPanes
}
