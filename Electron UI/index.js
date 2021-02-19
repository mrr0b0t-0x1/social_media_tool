const fs = require('fs')
const path = require('path')

const {spawn} = require('child_process');


btnSearch = document.getElementById('btnSearch')
btngetdata = document.getElementById('btngetdata')

userName = document.getElementById('userName')
fileContents = document.getElementById('fileContents')


let pathName = path.join(__dirname, 'Files')

//Handling Click Event for Search Btn ------------------------------------------
btnSearch.addEventListener('click', function(){
    //let file = path.join(pathName, userName.value)
    //let contents = fileContents.value
    // fs.writeFile(file, contents, function(err) {
    //     if(err) {
    //         return console.log(err);
    //     }

    // }); 
    //console.log("Name:"+ userName.value);

    const childPython = spawn('python', ['test.py',userName.value]);
    childPython.stdout.on('data', (data) => {
        console.log(`Python Script Output: ${data}`);
    })

});

//Handling Click event for Getdata Btn  --------------------------------------------------------

btngetdata.addEventListener('click', function(){
    var mysql = require('mysql');

    var connection = mysql.createConnection({
        host:"localhost",
        user:"root",
        password:null,
        database:"electron_test"
    });

    connection.connect((err) => {
        if(err){
            return console.log(err.stack);
        }

        console.log("Connection Established successfully");
    });


    //Execute the Query

    $queryString = 'SELECT * FROM `contacts` WHERE `id` = "2";';

    connection.query($queryString, (err, rows, fields) => {
        if(err)
        {
            return console.log("Some error occured",err);
        }
        console.log(rows);
    })


    connection.end(() => {
        console.log("Connection Successfully Closed");
    });
});
