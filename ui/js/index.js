const path = require('path');
const { PythonShell } = require('python-shell')
const kill = require('tree-kill');

$(document).ready(function () {
    const userName = document.getElementById('userName');
    const usernameForm = document.getElementById('usernameForm');
    const liveResults = document.getElementById('liveResults');
    const reindexDB = document.getElementById('reindexDB');
    const btnSearchUser = document.getElementById('btnSearchUser');
    const btnNewSearch = document.getElementById('btnNewSearch');
    const btnCancelSearch = document.getElementById('btnCancelSearch');
    const resultTabs = document.getElementById('resultTabs');
    const resultsTabContent = document.getElementById('results-tabContent');
    const btnUpdateData = document.getElementById('btnUpdateUserData');
    const btnRemoveData = document.getElementById('btnRemoveUserFromDB');
    const btnExportData = document.getElementById("btnExportData");

    // Import the get_data module to perform DB operations
    const { parseDBData, siteList, tabAndPanes, exportTables } = require( path.resolve(__dirname, './js/get_data.js') );

    // Toggle the live results box when "Search" or "New Search" button is clicked
    function toggleLiveResults() { $('#searchBox, #liveResults').toggleClass(
              'offset-1 col-sm-10 offset-sm-1 col-md-8 offset-md-2 col-lg-6 offset-lg-3').toggleClass(
                      'col-sm-6 col-md-6 col-lg-6');
    }

    let prevUserName = null

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

    // Create a python-shell instance
    function createPythonShell(args, btn) {

        const options = {
            mode: 'json',
            pythonPath: '../venv1/bin/python',
            pythonOptions: ['-u'], // get print results in real-time
            scriptPath: '../scripts',
            args: args
        };

        let data = false;

        // Create a python-shell instance
        const pyshell = new PythonShell('main.py', options);
        console.log("pyshell child pid: " + pyshell.childProcess.pid)

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
                parseDBData(userName.value, message.DATA);
                // Show appropriate divs and add border-radius to last div
                data = true;
                $('#user-resultTab > h4')[0].innerText = userName.value;
                $('#results-tab > a:first').addClass('active');
                $('#results-tabContent > div:first').addClass('show active');
                $('#results-tab > a:not(.d-none):last').css('border-radius', '0 0 10px 10px');
            }

            $("#liveResults > div").animate({
                scrollTop: $("#liveResults > div")[0].scrollHeight,
                animationTimingFunction: "ease-in-out"
            }, 1000);
        });

        // end the input stream and allow the process to exit
        pyshell.end(function (err,code,signal) {
            if (err) throw err;

            $(btnCancelSearch).attr('disabled', true)
            $(btnNewSearch).attr('disabled', false)

            if (btn === reindexDB) {
                showDismissableAlert({
                    'id': 'reindex-alert',
                    'class': 'alert-success',
                    'msg': 'Database re-indexed'
                });
            }
            else if (btn === btnCancelSearch) {
                showDismissableAlert({
                    'id': 'cancel-alert',
                    'class': 'alert-danger',
                    'msg': 'Operation cancelled!'
                });
            }
            else if (btn === btnSearchUser) {
                if (data) {
                    showDismissableAlert({
                        'id': 'done-alert',
                        'class': 'alert-success',
                        'msg': 'Done! Crunching data...'
                    });
                    setTimeout(function() {
                        $('#list-results-list').click()
                    }, 1000);
                } else {
                    showDismissableAlert({
                        'id': 'error-alert',
                        'class': 'alert-danger',
                        'msg': 'Snap! An error occurred'
                    });
                }
            }
            else if (btn === btnUpdateData) {
                showDismissableAlert({
                    'id': 'update-alert',
                    'class': 'alert-success',
                    'msg': 'User data updated!'
                });
            }
            else if (btn === btnRemoveData) {
                showDismissableAlert({
                    'id': 'remove-alert',
                    'class': 'alert-success',
                    'msg': 'User data removed!'
                });
            }

            console.log('The exit code was: ' + code);
            console.log('The exit signal was: ' + signal);
            console.log('finished');
        });

        return pyshell;
    }

    // Search or update user data
    function searchUpdateUser(operation) {
        // Create a python-shell instance to get user data
        let searchUser = createPythonShell(
            ['--username', userName.value, operation],
            (operation === "--search") ? btnSearchUser : btnUpdateData
        )

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

        $(btnCancelSearch).click(function () {
            // Kill python-shell and all running child processes
            kill(searchUser.childProcess.pid);
        });
    }

    // Show/Hide the "No results" div if results are empty/filled respectively
    $('body').on('DOMSubtreeModified', resultsTabContent, function () {
        if ($('#results-tabContent div[id^="nav-tabContent"] > div').text().trim() === '') {
            $(resultTabs).addClass('d-none');
            $('#noResults').removeClass('d-none');
        } else {
            $(resultTabs).removeClass('d-none');
            $('#noResults').addClass('d-none');
        }
    });
    // $('#list-results-list').click();

    // Re-index DB
    $(reindexDB).click( function () {
        showDismissableAlert({
            'id': 'reindexing-alert',
            'class': 'alert-primary',
            'msg': 'Re-indexing...'
        });
        createPythonShell(
            ['--reindex-db'],
            reindexDB
        )
    });

    // "Search" button actions
    $(btnSearchUser).click(function () {
        prevUserName = userName.value;

        showDismissableAlert({
            'id': 'search-alert',
            'class': 'alert-primary',
            'msg': 'Starting search...'
        });

        searchUpdateUser("--search");
    });

    // "New Search" button actions
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
            $('#results-tabContent div[id^="nav-tabContent"] > div').empty();
            $('#results-tab > a').removeClass('active');
            Object.keys(siteList).forEach(function (site) {
                $(tabAndPanes[siteList[site]][0]).addClass('d-none');
                $(tabAndPanes[siteList[site]][1]).addClass('d-none');
            });
        }
    });

    // "Cancel" button actions
    $(btnCancelSearch).click(function () {
        $(btnCancelSearch)
            .attr('disabled', true)
            .data('clicked', true)
        $(btnNewSearch).attr('disabled', false)

        liveResults.firstElementChild.innerHTML += "<span class='d-block'><span class='text-grey'>❯</span>&emsp;" +
            "<span class='text-danger'>Interrupted!</span> Search cancelled.</span>";
    });

    // "Update data" button actions
    $(btnUpdateData).click(function () {
        showDismissableAlert({
            'id': 'update-alert',
            'class': 'alert-primary',
            'msg': 'Updating data...'
        });
        $('#list-search-list').click();
        $(btnNewSearch).click();
        setTimeout( function () {
            $(userName).val(prevUserName);
            setTimeout( function () {
                searchUpdateUser("--update");
            }, 200);
        }, 1000);
    });

    // "Remove data" button actions
    $(btnRemoveData).click(function () {
        showDismissableAlert({
            'id': 'removing-alert',
            'class': 'alert-danger',
            'msg': 'Removing data...'
        });

        // Create a python-shell instance to remove user data
        createPythonShell(
            ['--remove-data', userName.value],
            btnRemoveData
        )
        $("#removeData").modal('hide');
        $(btnNewSearch).click();
        setTimeout(function () {
            $("#list-search-list").click();
            $(userName).focus();
        }, 300);
    });

    // "Export" button actions
    $(btnExportData).click( function () {
        showDismissableAlert({
            'id': 'export-alert',
            'class': 'alert-primary',
            'msg': 'Exporting...'
        });
        exportTables();
    })


    $("#results-tabContent > div[id^='list-'] .list-group").each( function (i, div) {
        if ($(div).children().length === 1) {
            $(div).children().css({
                "border": "1px solid #ddd",
                "border-radius": "10px"
            });
        }
    });
    // console.log($("#results-tabContent div > .list-group").children().length);
});
