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

const request = require('request');
const fs = require('fs');
const path = require('path');

let base_css = null;
fs.readFile(
    path.resolve(__dirname, '..' , 'node_modules', 'bootstrap', 'dist', 'css', 'bootstrap.min.css'),
    'utf8',
    function(err, data) {
        if (err) throw err;
        base_css = data;
});
let export_css = null;
fs.readFile(
    path.resolve(__dirname, '..', 'css', 'export.css'),
    'utf8',
    function(err, data) {
        if (err) throw err;
        export_css = data;
});

const sectionList = {
    "list-about-fb": "Facebook - About",
    "list-posts-fb": "Facebook - Posts",
    "list-about-insta": "Instagram - About",
    "list-posts-insta": "Instagram - Posts",
    "list-about-twitter": "Twitter - About",
    "list-timeline-twitter": "Twitter - Timeline",
    "list-about-reddit": "Reddit - About",
    "list-posts-reddit": "Reddit - Posts"
}

// Show a dismissable alert
function showDismissableAlert(alert) {
    if ($('#alertsView > div').text().trim() !== '') {
        $('.alert').alert('close');
        setTimeout(function () {
            showDismissableAlert(alert);
        }, 250);
    } else {
        $('#alertsView > div')[0].innerHTML =
            '<div id="' + alert['id'] + '" class="alert ' + alert['class'] + ' m-0 text-center fade" role="alert">' +
            alert['msg'] +
            '</div>';

        const el = document.getElementById(alert['id']);
        setTimeout(function () {
            $(el).addClass('show');
            setTimeout(function () {
                $(el).alert('close');
            }, 1995);
        }, 5);
    }
}

function fixLongStrings() {
    $("td:not(:empty):not(:has(table))").each( function( i ) {
        if (this.innerHTML.trim() !== '') {
            let str = this.innerHTML
            let arr = str.match(/.[^\n]{0,60}/g)
            this.innerHTML = arr.join("<br/>")
        }
    });
}

function createDir(dir) {
    try {
        if ( !fs.existsSync(dir) ) {
            fs.mkdirSync(dir, {recursive: true})
        }
        return true
    } catch (err) {
        return err
    }
}

function exportTableToFile(username, sections) {
    let doc = document.createElement('html');

    let all_data = document.createDocumentFragment();
    let head = document.createElement('head');
    let body = document.createElement('body');

    let style = document.createElement('style');
    style.innerHTML += base_css + "\n\n" + export_css;

    head.innerHTML += '<link rel="preconnect" href="https://fonts.gstatic.como">' +
        '<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@600&display=swap" rel="stylesheet">'
    head.appendChild(style);

    let h1 = document.createElement('h1')
    h1.innerHTML = "Searched username: " + username
    body.appendChild(h1);

    fixLongStrings();

    sections.forEach( function (section) {
        // if ( section.id !== 'list-overview-reddit') {
            let h3 = document.createElement('h3')
            h3.innerHTML = sectionList[ section.id ]

            body.append(
                document.createElement('br'),
                h3,
                document.createElement('br')
            );

            let div = document.createElement('div')
            div.innerHTML = section.innerHTML
            body.appendChild(div);

        // }
    });

    all_data.append( head, body );
    doc.append(all_data);

    // fs.writeFile(path.join(__dirname, "../../exports/table.html"), doc.innerHTML, err => {
    //     if (err) {
    //         console.log(err)
    //     }
    // });

    let opts = {
      uri: 'https://api.sejda.com/v2/html-pdf',
      headers: {
        'Authorization' : 'Token: ' + 'api_public_e1b64c3150a64267b95ca6d1b0477567',
      },
      json: {
          'htmlCode': doc.innerHTML,
          'viewportWidth': 1200,
          'pageSize': 'a4',
          'pageMargin': 1,
          'pageMarginUnits': 'cm'
      }
    };

    const dir = path.resolve(__dirname, '..', '..', 'exports', username)
    const res = createDir(dir)

    if ( res ) {
        request.post(opts)
            .on('error', function (err) {
                return console.error(err);
            })
            .on('response', function (response) {
                if (response.statusCode === 200) {
                    response.pipe(fs.createWriteStream(path.resolve(dir, username + '.pdf'), {flags: "w"}))
                        .on('finish', function () {
                            showDismissableAlert({
                                'id': 'export-success',
                                'class': 'alert-success',
                                'msg': 'Exported PDF to storage'
                            });
                            console.log('Exported PDF to storage');
                        });
                } else {
                    return console.error('Got code: ' + response.statusCode);
                }
            });
    } else {
        console.log(res)
        showDismissableAlert({
            'id': 'export-success',
            'class': 'alert-success',
            'msg': res
        });
    }
}

// Export modules
module.exports = {
    exportData: exportTableToFile
}
