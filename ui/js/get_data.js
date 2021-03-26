const fs = require('fs');

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
function traverseDataTree(obj, site, section, key=null) {
    let sectionName = "list" + section.split(username)[1];
    if (sectionName.includes("fb")) {
        sectionName = sectionName.substring(0, sectionName.lastIndexOf("-"));
    }

    const sectionElement = document.getElementById(sectionName);

    if (typeof obj === 'object') {
        if (Array.isArray(obj)) {
            for (const [idx, val] of obj.entries()) {
                if (typeof val === 'object')
                    traverseDataTree(val, site, section);
                else
                    if (idx !== obj.length - 1)
                        sectionElement.innerHTML += val + ", ";
                    else
                        sectionElement.innerHTML += val + "<br />";
            }
        }
        else {
            Object.keys(obj).forEach( function (key) {
                if (obj[key] !== null && obj[key].length !== 0) {
                    if (typeof obj[key] === 'object') {
                        sectionElement.innerHTML += key + ": <br />";
                        traverseDataTree(obj[key], site, section);
                    }
                    else
                        traverseDataTree(obj[key], site, section, key);
                }
            })
        }
    } else {
        if (key)
            sectionElement.innerHTML += key + ": " + obj + "<br />";
    }
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
                            traverseDataTree(data, site, key);
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
