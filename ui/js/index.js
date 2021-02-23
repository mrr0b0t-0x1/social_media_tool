$(document).ready(function () {
    const userName = document.getElementById('userName')
    const usernameForm = document.getElementById('usernameForm')
    const liveResults = document.getElementById('liveResults')
    const btnSearch = document.getElementById('btnSearch')
    const btnSearchAgain = document.getElementById('btnSearchAgain')
    const btnCancel = document.getElementById('btnCancel')
    const resultTabs = document.getElementById('resultTabs')

    function toggleLiveResults() { $('#searchBox, #liveResults').toggleClass(
              'offset-1 col-sm-10 offset-sm-1 col-md-8 offset-md-2 col-lg-6 offset-lg-3').toggleClass(
                      'col-sm-6 col-md-6 col-lg-6');
    }

    function traverse(obj, parent) {
        for (let key in obj) {
            if (obj.hasOwnProperty(key)) {
                if (typeof obj[key] === 'object') {
                    let el = document.createElement("div");
                    el.innerText = key + ": "
                    parent.appendChild(el);
                    traverse(obj[key], el);
                } else {
                    let txt = document.createElement("span");
                    txt.innerText = key + ": " + obj[key]
                    txt.innerHTML += "<br />"
                    parent.appendChild(txt);
                }
            }
        }
    }
    // $('#list-results-list').click()

    $('body').on('DOMSubtreeModified', resultTabs, function () {
        if ($(resultTabs).is(':empty')) {
            $(resultTabs).addClass('d-none')
            $('#noResults').removeClass('d-none')
        } else {
            $(resultTabs).removeClass('d-none')
            $('#noResults').addClass('d-none')
        }
    });

    $(btnSearch).click(function () {
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
                liveResults.firstElementChild.innerHTML += "<span class='d-block'><span class='text-grey'>❯</span>&emsp;<span class='text-danger'>Error: " + message.ERROR + "</span></span>"
                console.log("Error: " + message.ERROR);
            }
            else if (message.ELAPSED_TIME) {
                liveResults.firstElementChild.innerHTML += "<span class='d-block'><span class='text-grey'>❯</span>&emsp;<span class='text-success'>Done! Elapsed Time: " + message.ELAPSED_TIME + "</span></span>"
                console.log("Done! Elapsed time: " + message.ELAPSED_TIME);
            }
            else if (message.INFO) {
                liveResults.firstElementChild.innerHTML += "<span class='d-block'><span class='text-grey'>❯</span>&emsp;" + message.INFO + "</span>"
                console.log("Info: " + message.INFO);
            }
            else if (message.DATA) {
                liveResults.firstElementChild.innerHTML += "<span class='d-block'><span class='text-grey'>❯</span>&emsp;<span class='text-info'>Data Fetched!</span></span>"
                traverse(message.DATA, resultTabs);
                console.log("Data: ", message.DATA);
            }
        });

        // end the input stream and allow the process to exit
        pyshell.end(function (err,code,signal) {
            if (err) throw err;
            $(btnCancel).attr('disabled', true)
            $(btnSearchAgain).attr('disabled', false)
            setTimeout(function() {
                $('#list-results-list').click()
            }, 500);
            console.log('The exit code was: ' + code);
            console.log('The exit signal was: ' + signal);
            console.log('finished');
        });


        // Make changes in UI
        if ($(liveResults).hasClass('hide')) {
            setTimeout(function () {
                $(liveResults).removeClass('hide').addClass('show');
                $(btnSearchAgain).attr('disabled', true);
                $(btnCancel).attr('disabled', false)

                setTimeout(function () {
                    $(liveResults).removeClass('d-none');
                    $(btnSearch).addClass('d-none').attr('disabled', true);
                    $('#btnSearchAgain').removeClass('d-none');
                    setTimeout(function (){
                       $('#btnSearchAgain, #btnCancel').removeClass('hide').addClass('show');
                    }, 50);
                }, 50);

            }, 500);

            toggleLiveResults();
            $(userName).attr('disabled', true);
            $(btnSearch).removeClass('show').addClass('hide');

            liveResults.firstElementChild.innerHTML += "<span class='d-block'><span class='text-grey'>❯</span>&emsp;<span class='text-info'>Starting search...</span></span>";
        }

        $(btnCancel).click(function (){
            pyshell.kill()
        });
    });

    $(btnSearchAgain).click(function () {
        if ($(liveResults).hasClass('show')) {
            setTimeout(function() {
                toggleLiveResults();
                $(liveResults).addClass('d-none');
                $(userName).attr('disabled', false);
                $(btnSearch).removeClass('d-none');
                $('#btnSearchAgain').addClass('d-none');

                setTimeout(function () {
                   $(btnSearch).removeClass('hide').addClass('show');
                }, 100);

                $(usernameForm)[0].reset();
                $(userName).focus();
                liveResults.firstElementChild.innerHTML = '';
            }, 500);

            $(liveResults).removeClass('show').addClass('hide');
            $(btnSearch).attr('disabled', false);
            $('#btnSearchAgain, #btnCancel').removeClass('show').addClass('hide');
            $(resultTabs).empty();
        }
    });

    $(btnCancel).click(function (){
        $(btnCancel).attr('disabled', true)
        $(btnSearchAgain).attr('disabled', false)

        liveResults.firstElementChild.innerHTML += "<span class='d-block'><span class='text-grey'>❯</span>&emsp;<span class='text-danger'>Interrupted!</span> Search cancelled.</span>";
    });
});
