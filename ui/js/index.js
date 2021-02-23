let userName = document.getElementById('userName')

let btnSearch = document.getElementById('btnSearch')
//Handling Click Event for Search Btn ------------------------------------------
btnSearch.addEventListener('click', function(){
    let {PythonShell} = require('python-shell')

    let options = {
        mode: 'json',
        pythonPath: '../venv1/bin/python',
        pythonOptions: ['-u'], // get print results in real-time
        scriptPath: '../scripts',
        args: [userName.value]
    };

    // PythonShell.run('main.py', options, function (err, results) {
    //   if (err) throw err;
    //   // results is an array consisting of messages collected during execution
    //   //   let resultView = document.getElementById('resultView')
    //     let dataView = document.getElementById('dataView')
    //     let errorView = document.getElementById('errorView')
    //     let elapsedTime = document.getElementById('elapsedTime')
    //
    //     // results.forEach(function (obj) {
    //     //     if (obj.ERROR) {
    //     //         errorView.innerHTML = "<div class='col-12'>Error: " + obj.ERROR + "</div>"
    //     //         console.log("Error: " + obj.ERROR);
    //     //     }
    //     //     else if (obj.ELAPSED_TIME) {
    //     //         elapsedTime.innerHTML = "<div class='col-12'>Error: " + obj.ELAPSED_TIME + "</div>"
    //     //         console.log("Elapsed time: " + obj.ELAPSED_TIME);
    //     //     }
    //     //     else if (obj.DATA) {
    //     //         dataView.innerHTML = "<div class='col-12'>Error: " + obj.DATA + "</div>"
    //     //         console.log("Data: ", obj.DATA);
    //     //     }
    //     // });
    //   // console.log(results);
    // });

    // // Create a pyshell
    const pyshell = new PythonShell('main.py', options);

    const liveResults = document.getElementById('liveResults')

    // // sends a message to the Python script via stdin
    // pyshell.send(userName.value);

    pyshell.on('message', function (message) {
      // received a message sent from the Python script (a simple "print" statement)
      console.log(message);

      if (message.ERROR) {
            liveResults.firstElementChild.innerHTML += "<span class='d-block'>>&emsp;<span class='text-danger'>Error:</span> " + message.ERROR +"</span>"
            console.log("Error: " + message.ERROR);
        }
        else if (message.ELAPSED_TIME) {
            liveResults.firstElementChild.innerHTML += "<span class='d-block'>>&emsp;<span class='text-success'>Elapsed Time:</span> " + message.ELAPSED_TIME +"</span>"
            console.log("Elapsed time: " + message.ELAPSED_TIME);
        }
        else if (message.DATA) {
            liveResults.firstElementChild.innerHTML += "<span class='d-block'>>&emsp;<span class='text-info'>Data:</span> " + message.DATA +"</span>"
            console.log("Data: ", message.DATA);
        }
    });
    //
    // // end the input stream and allow the process to exit
    // pyshell.end(function (err,code,signal) {
    //   if (err) throw err;
    //   // console.log('The exit code was: ' + code);
    //   // console.log('The exit signal was: ' + signal);
    //   // console.log('finished');
    // });
});
