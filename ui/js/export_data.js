const request = require('request');
const fs = require('fs');
const path = require('path');

let base_css = null;
fs.readFile(
    path.join(__dirname, "../node_modules/bootstrap/dist/css/bootstrap.min.css"),
    'utf8',
    function(err, data) {
        if (err) throw err;
        base_css = data;
});
let export_css = null;
fs.readFile(
    path.join(__dirname, "../css/export.css"),
    'utf8',
    function(err, data) {
        if (err) throw err;
        export_css = data;
});

const sectionList = {
    "list-about-fb": "Facebook - About",
    "list-posts-fb": "Facebook - Posts",
    "list-about-instagram": "Instagram - About",
    "list-about-twitter": "Twitter - About",
    "list-timeline-twitter": "Twitter - Timeline",
    "list-about-reddit": "Reddit - About",
    "list-overview-reddit": "Reddit - Overview"
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
    head.appendChild(style);

    let h1 = document.createElement('h1')
    h1.innerHTML = "Username: " + username
    body.appendChild(h1);

    fixLongStrings();

    sections.forEach( function (section) {
        if ( section.id !== 'list-overview-reddit') {
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

        }
    });

    all_data.append( head, body );
    doc.append(all_data);

    // console.log(all_data);

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

    const dir = path.join(__dirname, "../../exports/" + username)
    const res = createDir(dir)

    if ( res ) {
        request.post(opts)
            .on('error', function (err) {
                return console.error(err);
            })
            .on('response', function (response) {
                if (response.statusCode === 200) {
                    response.pipe(fs.createWriteStream(path.join(dir, username + '.pdf')))
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
