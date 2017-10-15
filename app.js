/*-----------------------------------------------------------------------------
A simple echo bot for the Microsoft Bot Framework.
-----------------------------------------------------------------------------*/
// This loads the environment variables from the .env file
// #ifdef ENV
// require('dotenv-extended').load();
// #endif

var restify = require('restify');
var builder = require('botbuilder');

// Setup Restify Server
var server = restify.createServer();
server.listen(process.env.port || process.env.PORT || 3978, function() {
  console.log('%s listening to %s', server.name, server.url);
});

// Create chat connector for communicating with the Bot Framework Service
var connector = new builder.ChatConnector({
  appId: process.env.MicrosoftAppId,
  appPassword: process.env.MicrosoftAppPassword,
  stateEndpoint: process.env.BotStateEndpoint,
  openIdMetadata: process.env.BotOpenIdMetadata
});

// Listen for messages from users
server.post('/api/messages', connector.listen());

/*----------------------------------------------------------------------------------------
 * Bot Storage: This is a great spot to register the private state storage for your bot.
 * We provide adapters for Azure Table, CosmosDb, SQL Azure, or you can implement your own!
 * For samples and documentation, see: https://github.com/Microsoft/BotBuilder-Azure
 * ---------------------------------------------------------------------------------------- */

// Create your bot with a function to receive messages from the user
var bot = new builder.UniversalBot(connector, function(session) {
  session.send(
    'Sorry, I did not understand \'%s\'. Type \'help\' if you need assistance.',
    session.message.text);
  session.endDialog();
});

// Main dialog with LUIS
const LUIS_URL =
  "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/99e54023-bf56-4417-8311-fa5eb2d7245e?subscription-key=a659eee201024a6d92b6cf9a2973374a&timezoneOffset=0&verbose=true&q=";
// https://github.com/Microsoft/BotBuilder/issues/2670
// enables not rezognizing for prompts
// something says that IntentDialo may be better; switch to it if further problems?
var recognizer = new builder.LuisRecognizer(LUIS_URL).onEnabled(function(
  context, callback) {
  var enabled = context.dialogStack().length == 0;
  callback(null, enabled);
});
bot.recognizer(recognizer);

bot.dialog('Greeting', function(session) {
  // parent(session);
  session.endDialog();
}).triggerAction({
  matches: 'Greeting'
});

bot.dialog('Help', function(session) {
  session.endDialog(
    'Welcome to STRAT! We make it easy to learn about your favorite companies, and suggest stocks based on your preferences, to get started, take our profile test by saying "Risk Profile"!'
  );
}).triggerAction({
  matches: 'Help'
});

bot.dialog('Info', function(session, args) {
  var stockEntity = builder.EntityRecognizer.findEntity(args.intent.entities,
    'Stock');
  parent(session, "info", stockEntity.entity);
  session.endDialog();
}).triggerAction({
  matches: 'Info'
});

bot.dialog('Learn', function(session, args) {
  var stockEntity = builder.EntityRecognizer.findEntity(args.intent.entities,
    'Stock');
  parent(session, "learn", stockEntity.entity);
  session.endDialog();
}).triggerAction({
  matches: 'Learn'
});

bot.dialog('Profile', [
  function(session) {
    session.userData.rating = 0;
    // Prompt user for next field
    builder.Prompts.choice(session, "How long do you hold a stock?", [
      "Less than 1 year",
      "1 to 2 years",
      "2 to 3 years",
      "3 to 4 years",
      "4 to 5 years",
      "More than 5 years"
    ], {
      listStyle: builder.ListStyle.button
    });
  },
  function(session, result) {
    session.userData.rating += (result.response.index * 2);
    builder.Prompts.choice(session,
      "Which of the following have you owned before or own now?", [
        "N/A",
        "Time deposit or money market funds",
        "Bonds or bond mutual funds",
        "Stock mutual funds",
        "Individual stocks",
        "Leveraged funds"
      ], {
        listStyle: builder.ListStyle.button
      });
  },
  function(session, result) {
    session.userData.rating += (result.response.index * 2);
    builder.Prompts.choice(session,
      "Which best describes your experience of investment?", [
        "None",
        "None beyond bank savings accounts",
        "Some investment experience (mutual funds or individual shares)",
        "Experienced with a portfolio managed by an advisor",
        "Experienced and manage my own portfolio",
        "Buy AMD"
      ], {
        listStyle: builder.ListStyle.button
      }

    );
  },
  function(session, result) {
    session.userData.rating += (result.response.index * 2);
    builder.Prompts.choice(session,
      "What is your prime objective with investment?", [
        "Education of your children",
        "Savings",
        "Capital growth and returns",
        "Retirement",
        "My legacy",
        "Yacht"
      ], {
        listStyle: builder.ListStyle.button
      }
    );
  },
  function(session, result) {
    session.userData.rating += (result.response.index * 2);
    builder.Prompts.choice(session,
      "What percentage of your total savings are invested?", [
        "<10%",
        "10-20%",
        "20-30%",
        "30-40%",
        "40-99%",
        "100%"
      ], {
        listStyle: builder.ListStyle.button
      }
    );
  },
  function(session, result) {
    session.userData.rating += (result.response.index * 2);
    builder.Prompts.choice(session,
      "If you were to invest all your savings into only one of the five investments below, which would you choose?\nChoice             |  Worst Year  |  Average Year  |  Best Year", [
        "Investment A   |  4 %              |   6 %                |  8 %",
        "Investment B   |  2 %              |   8 %                |  14 %",
        "Investment C   | -5 %              |   10 %               |  20 %",
        "Investment D   | -15 %             |   12 %               |  25 %",
        "Investment E   | -20 %             |   15 %               |  30 %",
        "Investment F   | -80 %             |   50 %               |  150 %"
      ], {
        listStyle: builder.ListStyle.button
      }
    );
  },
  function(session, result) {
    session.userData.rating += (result.response.index * 2);
    builder.Prompts.choice(session,
      "What sport would you most like to participate in?", [
        "Baseball",
        "Soccer",
        "Skiing",
        "Rock Climbing",
        "Skydiving",
        "Wingsuit Flying"
      ], {
        listStyle: builder.ListStyle.button
      }
    );
  },
  function(session, result) {
    session.userData.rating += (result.response.index * 2);
    builder.Prompts.choice(session,
      "Which country would you be least likely to visit?", [
        "Venezuela",
        "Mexico",
        "Russia",
        "The United Kingdom",
        "Germany",
        "Iceland"
      ], {
        listStyle: builder.ListStyle.button
      }
    );
  },
  function(session, result) {
    session.userData.rating += (result.response.index * 2);
    builder.Prompts.choice(session,
      "How many bones have you broken?", [
        "0",
        "1-2",
        "3-5",
        "6-9",
        "10-14",
        "15+"
      ], {
        listStyle: builder.ListStyle.button
      }
    );
  },
  function(session, result) {
    session.userData.rating += (result.response.index * 2);
    builder.Prompts.choice(session,
      "Which of these describes you most accurately?", [
        "Cross the street only at crosswalks",
        "Cross the street near crosswalks",
        "Cross the street anywhere if you don’t see cars",
        "Cross the street anywhere if there are no cars in your path",
        "Cross the street anywhere if the cars are moving slowly or have room to stop",
        "Cross the street anywhere, no matter what"
      ], {
        listStyle: builder.ListStyle.button
      }
    );
  },
  function(session, result) {
    session.userData.rating += (result.response.index * 2);
    session.userData.rating >= 50 ? session.userData.rating /= 250 :
      session.userData.rating /= 500;
    session.userData.rating == 0.4 ? session.userData.rating = 1 : session.userData
      .rating = session.userData.rating;
    session.send("Your risk score is: %s", session.userData.rating);
    session.endDialog();
  }
]).triggerAction({
  matches: 'Profile'
});

bot.dialog('Suggest', function(session, args) {
  parent(session, "suggest", session.userData.rating);
  session.endDialog();
}).triggerAction({
  matches: 'Suggest'
});

// JS -> PYTHON code
// https://gist.github.com/cowboy/3427148

var parent = function(session, type, stock) {
  var spawn = require('child_process').spawn;
  var child = spawn('python3', ['-u', 'python-scripts/res.py', type, stock]);
  var stdout = '';
  var stderr = '';
  child.stdout.on('data', function(buf) {
    stdout += buf;
  });
  child.stderr.on('data', function(buf) {
    stderr += buf;
  });
  child.on('close', function(code) {
    // session.send('[END] code %s', code);
    session.send(stdout);
    if (stderr) {
      session.send('[END] stderr "%s"', stderr);
    }
  });
};

// log any bot errors into the console
bot.on('error', function(e) {
  console.log('And error ocurred', e);
});
