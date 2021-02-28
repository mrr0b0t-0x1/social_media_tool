const fs = require('fs');

$(document).ready(function () {
    const userName = document.getElementById('userName');
    const usernameForm = document.getElementById('usernameForm');
    const liveResults = document.getElementById('liveResults');
    const btnSearchUser = document.getElementById('btnSearchUser');
    const btnNewSearch = document.getElementById('btnNewSearch');
    const btnCancelSearch = document.getElementById('btnCancelSearch');
    const resultTabs = document.getElementById('resultTabs');
    const resultsTabContent = document.getElementById('results-tabContent');
    const btnUpdateData = document.getElementById('btnUpdateUserData');
    const btnRemoveData = document.getElementById('btnRemoveUserFromDB');
    const alertsView = document.getElementById('alertsView');

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
    }

    function toggleLiveResults() { $('#searchBox, #liveResults').toggleClass(
              'offset-1 col-sm-10 offset-sm-1 col-md-8 offset-md-2 col-lg-6 offset-lg-3').toggleClass(
                      'col-sm-6 col-md-6 col-lg-6');
    }

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

    function readJSONFile(path, callback) {
        try {
            const data = fs.readFileSync(path);
            const dataJSON = JSON.parse(data.toString());
            return callback && callback(null, dataJSON);
        } catch (err) {
            return callback && callback(err);
        }
    }
    function traverseDataTree(obj, site) {
        Object.keys(obj).forEach(function (key) {
            // console.log(key);
            if (obj[key] !== null) {
                if (obj[key] !== null && typeof obj[key] === 'object')
                    traverseDataTree(obj[key], site);
                else {
                    tabAndPanes[site][1].innerHTML += key + ": " + obj[key] + "<br />"
                    // console.log(nestKey + " -> " + key + ": " + obj[key]);
                    // let txt = document.createElement("span");
                    // txt.innerText = key + ": " + obj[key]
                    // txt.innerHTML += "<br />"
                    // parent.appendChild(txt);
                }
            }
        });
    }
    function traverseDBTree(obj, site) {
        Object.keys(obj).forEach(function (key) {
            console.log(key);
            if (obj[key] !== null) {
                if (obj[key] !== null && typeof obj[key] === 'object')
                    traverseDBTree(obj[key], site);
                else {
                    if (obj[key].split('.').pop() === 'json') {
                        readJSONFile(obj[key], (err, data) => {
                            if (err) {
                                console.log(err);
                            } else {
                                console.log(data);
                                traverseDataTree(data, site);
                            }
                        });
                    }
                    // tabAndPanes[site][1].innerHTML += key + ": " + obj[key] + "<br />"
                    // console.log(nestKey + " -> " + key + ": " + obj[key]);
                    // let txt = document.createElement("span");
                    // txt.innerText = key + ": " + obj[key]
                    // txt.innerHTML += "<br />"
                    // parent.appendChild(txt);
                }
            }
        });
    }
    function parseDBData(obj) {
        // console.log(Object.keys(obj));
        Object.keys(obj['sites_found']).forEach(function (site) {
            if (siteList.includes(site)) {
                // show those tabs whose sites are found
                $(tabAndPanes[site][0]).removeClass('d-none');
                $(tabAndPanes[site][1]).removeClass('d-none');

                traverseDBTree(obj['sites_found'][site], site);
            }
        });
    }

    // $('#results-tab').children().first().css(
    //     'border-radius', '10px 10px 0 0'
    // )

    $('body').on('DOMSubtreeModified', resultsTabContent, function () {
        if ($('#results-tabContent > div').text().trim() === '') {
            $(resultTabs).addClass('d-none')
            $('#noResults').removeClass('d-none')
        } else {
            $(resultTabs).removeClass('d-none')
            $('#noResults').addClass('d-none')
        }
    });


    $(btnSearchUser).click(function () {
        showDismissableAlert({
            'id': 'search-alert',
            'class': 'alert-primary',
            'msg': 'Starting search...'
        });
        // Execute backend script
        let {PythonShell} = require('python-shell')

        let options = {
            mode: 'json',
            pythonPath: '../venv1/bin/python',
            pythonOptions: ['-u'], // get print results in real-time
            scriptPath: '../scripts',
            args: [userName.value]
        };

        // Create a python-shell instance
        const pyshell = new PythonShell('main.py', options);

        const liveResults = document.getElementById('liveResults')

        pyshell.on('message', function (message) {
            // Received a message sent from the Python script (a simple "print" statement)
            if (message.ERROR) {
                liveResults.firstElementChild.innerHTML += "<span class='d-block'><span class='text-grey'>❯</span>" +
                    "&emsp;<span class='text-danger'>Error: " + message.ERROR + "</span></span>"
                console.log("Error: " + message.ERROR);
            }
            else if (message.ELAPSED_TIME) {
                liveResults.firstElementChild.innerHTML += "<span class='d-block'><span class='text-grey'>❯</span>" +
                    "&emsp;<span class='text-success'>Done! Elapsed Time: " + message.ELAPSED_TIME + "</span></span>"
                console.log("Done! Elapsed time: " + message.ELAPSED_TIME);
            }
            else if (message.INFO) {
                liveResults.firstElementChild.innerHTML += "<span class='d-block'><span class='text-grey'>❯</span>" +
                    "&emsp;" + message.INFO + "</span>"
                console.log("Info: " + message.INFO);
            }
            else if (message.DATA) {
                liveResults.firstElementChild.innerHTML += "<span class='d-block'><span class='text-grey'>❯</span>" +
                    "&emsp;<span class='text-info'>Data Fetched!</span></span>"
                parseDBData(message.DATA);
                // Show appropriate divs and add border-radius to last div
                $('#user-resultTab > h4')[0].innerText = userName.value;
                $('#results-tab > a:first').addClass('active');
                $('#results-tabContent > div:first').addClass('show active');
                $('#results-tab > a:not(.d-none):last').css('border-radius', '0 0 10px 10px');
            }
        });

        // end the input stream and allow the process to exit
        pyshell.end(function (err,code,signal) {
            if (err) throw err;
            $(btnCancelSearch).attr('disabled', true)
            $(btnNewSearch).attr('disabled', false)

            showDismissableAlert({
                'id': 'done-alert',
                'class': 'alert-success',
                'msg': 'Done! Crunching data...'
            });
            setTimeout(function() {
                $('#list-results-list').click()
            }, 1000);
            console.log('The exit code was: ' + code);
            console.log('The exit signal was: ' + signal);
            console.log('finished');
        });


        // Make changes in UI
        if ($(liveResults).hasClass('hide')) {
            setTimeout(function () {
                $(liveResults).removeClass('d-none');
                $(btnNewSearch).attr('disabled', true);
                $(btnCancelSearch).attr('disabled', false)

                setTimeout(function () {
                    $(liveResults).removeClass('hide').addClass('show');
                    $(btnSearchUser).addClass('d-none').attr('disabled', true);
                    $('#btnNewSearch').removeClass('d-none');
                    setTimeout(function (){
                       $('#btnNewSearch, #btnCancelSearch').removeClass('hide').addClass('show');
                    }, 50);
                }, 50);

            }, 500);

            toggleLiveResults();
            $(userName).attr('disabled', true);
            $(btnSearchUser).removeClass('show').addClass('hide');

            liveResults.firstElementChild.innerHTML += "<span class='d-block'><span class='text-grey'>❯</span>&emsp;" +
                "<span class='text-info'>Starting search...</span></span>";
        }

        $(btnCancelSearch).click(function (){
            pyshell.kill()
        });
    });

    $(btnNewSearch).click(function () {
        if ($(liveResults).hasClass('show')) {
            setTimeout(function() {
                toggleLiveResults();
                $(liveResults).addClass('d-none');
                $(userName).attr('disabled', false);
                $(btnSearchUser).removeClass('d-none');
                $('#btnNewSearch').addClass('d-none');

                setTimeout(function () {
                   $(btnSearchUser).removeClass('hide').addClass('show');
                }, 100);

                $(usernameForm)[0].reset();
                $(userName).focus();
                liveResults.firstElementChild.innerHTML = '';
            }, 500);

            $(liveResults).removeClass('show').addClass('hide');
            $(btnSearchUser).attr('disabled', false);
            $('#btnNewSearch, #btnCancelSearch').removeClass('show').addClass('hide');
            $('#results-tabContent > div').empty().removeClass('show active');
            $('#results-tab > a').removeClass('active');
            Object.keys(siteList).forEach(function (site) {
                $(tabAndPanes[siteList[site]][0]).addClass('d-none');
                $(tabAndPanes[siteList[site]][1]).addClass('d-none');
            });
        }
    });

    $(btnCancelSearch).click(function () {
        $(btnCancelSearch)
            .attr('disabled', true)
            .data('clicked', true)
        $(btnNewSearch).attr('disabled', false)

        liveResults.firstElementChild.innerHTML += "<span class='d-block'><span class='text-grey'>❯</span>&emsp;" +
            "<span class='text-danger'>Interrupted!</span> Search cancelled.</span>";
    });

    $(btnUpdateData).click(function () {
        showDismissableAlert({
            'id': 'update-alert',
            'class': 'alert-success',
            'msg': 'Update button clicked'
        });
    });

    $(btnRemoveData).click(function () {
        showDismissableAlert({
            'id': 'remove-alert',
            'class': 'alert-danger',
            'msg': 'Remove button clicked'
        });
    });
});
