// YOU CAN USE THIS FILE AS REFERENCE FOR SERVER DEVELOPMENT

// include the express modules
var express = require("express");

// create an express application
var app = express();
const url = require('url');

// helps in extracting the body portion of an incoming request stream
var bodyparser = require('body-parser');

// fs module - provides an API for interacting with the file system
var fs = require("fs");

// helps in managing user sessions
var session = require('express-session');

// include the mysql module
var mysql = require("mysql");

// Bcrypt library for comparing password hashes
const bcrypt = require('bcrypt');

// A possible library helps reading uploaded file.
var formidable = require('formidable');
const e = require("express");



app.set('view engine', 'pug');
// apply the body-parser middleware to all incoming requests
app.use(bodyparser());

// use express-session
// in mremory session is sufficient for this assignment
app.use(session({
  secret: "csci4131secretkey",
  saveUninitialized: true,
  resave: false
}
));
// server listens on port 9007 for incoming connections
app.listen(9007, function(err){
  if (err) console.log("Error in server setup")
  console.log("Server listening on Port 9007");
})

// function to return the welcome page
app.get('/',function(req, res) {
  res.render(__dirname + '/client/welcome', { title: 'Welcome to Node.js'});
});


app.get('/login.html', function(req, res) {
  res.render(__dirname + '/client/login', { title: 'login', message: ''});
})

app.post('/loginPost', function(req, res) {
  const username = req.body.username;
  const password = req.body.password;

  if (username && password) {
    const connection = mysql.createConnection({
      host: 'cse-mysql-classes-01.cse.umn.edu',
      user: 'C4131NF23U27',
      password: '779',
      database: 'C4131NF23U27'
    });

    connection.connect();

    connection.query('SELECT * FROM tbl_accounts WHERE acc_login = ?', [username], function(error, results) {
      if (error) {
        throw error;
      } 
      if (results.length > 0) {
        const user = results[0];
        bcrypt.compare(password, user.acc_password, function(err, result) {
          if (result) {
            req.session.curuser = true;
            req.session.username = username;
            res.redirect('/schedule.html');
          } else {
            res.render(__dirname + '/client/login', { title: 'login', message: 'Incorrect username and/or password' });
          }
        });
      } else {
        res.render(__dirname + '/client/login', { title: 'login', message: 'Incorrect username and/or password' });
      }
    });

    connection.end();
  } else {
    res.render(__dirname + '/client/login', { title: 'login', message: 'Please enter a username and password' });
  }
});

// middle ware to serve static files
app.use('/client', express.static(__dirname + '/client'));

app.get('/welcome.html',function(req, res) {
  res.render(__dirname + '/client/welcome', { title: 'Welcome to Node.js'});
});

app.get('/schedule.html', function(req, res) {
  // res.sendFile(__dirname + '/client/schedule.html');
  if (req.session.curuser) {
    res.sendFile(__dirname + '/client/schedule.html');
    // res.render(__dirname + '/client/schedule', { title: 'My Schedule'});
  } else {
    res.redirect('/login.html');
  }
})

app.get('/logout', function(req, res) {
  if (req.session.curuser) {
    req.session.destroy(function(err) {
      if (err) {
        console.error(err);
      } else {
        console.log('Session destroyed');
        res.redirect('/');
      }
    });
  } else {
    console.log('Not logged in – session not set');
  }
});

app.get('/getSchedule', function(req, res) {
  // console.log(req.session);

  var q = url.parse(req.url, true);
  var day = q.query.day;
  var finalJson = [];
  
  const connection = mysql.createConnection({
    host: 'cse-mysql-classes-01.cse.umn.edu',
    user: 'C4131NF23U27',
    password: '779',
    database: 'C4131NF23U27'
  });

  connection.connect();
  connection.query('SELECT * FROM tbl_events WHERE event_day = ?', [day], function(error, results) {
    // console.log(results);
    if(results.length > 0) {
      for(let i = 0; i<results.length; i++) {
        var curobj = {}
        var capLetter = results[i].event_day.charAt(0).toUpperCase();
        var day_substr = results[i].event_day.slice(1);
        curobj.id = results[i].event_id;
        curobj.day = capLetter + day_substr;
        curobj.name = results[i].event_event;
        curobj.start = results[i].event_start;
        curobj.end = results[i].event_end;
        curobj.location = results[i].event_location;
        curobj.phone = results[i].event_phone;
        curobj.info = results[i].event_info;
        curobj.url = results[i].event_url;
        finalJson.push(curobj);
      }
    }

    // functi

    res.json(finalJson);
    res.end();
  })

  connection.end();
})

app.get('/addEvent.html', function(req, res) {
  if (req.session.curuser) {
    res.render(__dirname + '/client/addEvent', { title: 'Add Event'});
  } else {
    res.redirect('/login.html');
  }
})

app.post('/postEventEntry', function (req, res) {

  if(req.body.fileInp) {
    fs.readFile(req.body.fileInp, function (error, jsonString){
      if(error) {
        throw error;
      }

      // console.log(JSON.parse(jsonString));
      const connection = mysql.createConnection({
        host: 'cse-mysql-classes-01.cse.umn.edu',
        user: 'C4131NF23U27',
        password: '779',
        database: 'C4131NF23U27'
      });
      
      var days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];

      var events = JSON.parse(jsonString);
      // console.log(events);
      var loop = true;
      var i = 0;
      var j = 0;

      while(loop) {
        if(i == 6) {
          break;
        }
        if(j == events[days[i]].length - 1 || j == events[days[i]].length) {
          i++;
          j = 0;
        }

        if(events[days[i]].length == 0) {
          i++;
          j = 0;
        }

        // var curDay = events[days[i]]
        var curEvent = events[days[i]][j];
        const newEvent = {
          event_id: 0,
          event_day: days[i],
          event_event: curEvent.name,
          event_start: curEvent.start,
          event_end: curEvent.end,
          event_location: curEvent.location,
          event_phone: curEvent.phone,
          event_info: curEvent.info,
          event_url: curEvent.url
        }

        j++;

        connection.query('INSERT tbl_events SET ?', newEvent, function(error, results) {
          if(error) {
            throw error;
          }

        })
        
        console.log(newEvent)
      }
    })
  }
  const newEvent = {
    event_id: 0,
    event_day: req.body.day,
    event_event: req.body.event,
    event_start: req.body.start,
    event_end: req.body.end,
    event_location: req.body.location,
    event_phone: req.body.phone,
    event_info: req.body.info,
    event_url: req.body.start
  }

  const connection = mysql.createConnection({
    host: 'cse-mysql-classes-01.cse.umn.edu',
    user: 'C4131NF23U27',
    password: '779',
    database: 'C4131NF23U27'
  });
  // console.log(req.body);
  connection.connect();
  connection.query('INSERT tbl_events SET ?', newEvent, function(error, results) {
    if(error) {
      throw error;
    }
    else {
      res.redirect('client/schedule.html')
    }
    connection.end();
  })
  // console.log(req.body.event);
})

app.delete('/deleteEvent/:id', function(req, res) {
  if (req.session.curuser) {
    const eventId = req.params.id;
    
    const connection = mysql.createConnection({
      host: 'cse-mysql-classes-01.cse.umn.edu',
      user: 'C4131NF23U27',
      password: '779',
      database: 'C4131NF23U27'
    });

    connection.connect();
    connection.query('DELETE FROM tbl_events WHERE event_id = ?', [eventId], function(error, results) {
      if (error) {
        console.error(error);
        res.sendStatus(500);
      } else {
        res.sendStatus(200);
      }
    });

    connection.end();
  } else {
    res.redirect('/login.html');
  }
});
app.get('/editEvent.html', function(req, res) {
  res.render(__dirname + '/client/editEvent', { title: 'Edit Event', event: null });
})
app.get('/schedule/edit/:eventID', function(req, res) {
  if (req.session.curuser) {
    const eventID = req.params.eventID;

    const connection = mysql.createConnection({
      host: 'cse-mysql-classes-01.cse.umn.edu',
      user: 'C4131NF23U27',
      password: '779',
      database: 'C4131NF23U27'
    });
    connection.connect();
    connection.query('SELECT * FROM tbl_events WHERE event_id = ?', [eventID], function(error, results) {
      if (error) {
        throw error;
      }
      if (results.length > 0) {
        const eventData = results[0];
        console.log(eventData);

        res.render(__dirname + '/client/editEvent', { title: 'Edit Event', event: eventData });
      } else {
        res.status(404).send('Event not found');
      }
    });

    connection.end();
  } else {
    res.redirect('/login.html');
  }
});

app.post('/schedule/edit/:eventID', function(req, res) {
  if (req.session.curuser) {
    console.log(req);
    const eventID = req.params.eventID;
    const updatedEvent = req.body;

    console.log(updatedEvent);

    const connection = mysql.createConnection({
      host: 'cse-mysql-classes-01.cse.umn.edu',
      user: 'C4131NF23U27',
      password: '779',
      database: 'C4131NF23U27'
    });

    connection.connect();
    connection.query('UPDATE tbl_events SET event_event = ?, event_start = ?, event_end = ?, event_location = ?, event_phone = ?, event_info = ?, event_url = ? WHERE event_id = ?',
      [updatedEvent.event, updatedEvent.start, updatedEvent.end, updatedEvent.location, updatedEvent.phone, updatedEvent.info, updatedEvent.url, eventID],
      function(error, results) {
        if (error) {
          res.status(422).send('Error updating event');
        } else {
          res.redirect('/schedule.html');
        }
      });

    connection.end();
  } else {
    res.redirect('/login.html');
  }
});

// function to return the 404 message and error to client
app.get('*', function(req, res) {
  // add details
  res.sendStatus(404);
});
