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
});

// Main dialog with LUIS
const LUIS_URL =
  "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/99e54023-bf56-4417-8311-fa5eb2d7245e?subscription-key=a659eee201024a6d92b6cf9a2973374a&timezoneOffset=0&verbose=true&spellCheck=true&q=";
// https://github.com/Microsoft/BotBuilder/issues/2670
// enables not rezognizing for prompts
// something says that IntentDialo may be better; switch to it if further problems?
var recognizer = new builder.LuisRecognizer(LUIS_URL).onEnabled(function(
  context, callback) {
  var enabled = context.dialogStack().length == 0;
  callback(null, enabled);
});
bot.recognizer(recognizer);

bot.dialog('Help', function(session) {
  session.endDialog(
    'Hi! Try asking me things like \'search hotels in Seattle\', \'search hotels near LAX airport\' or \'show me the reviews of The Bot Resort\''
  );
}).triggerAction({
  matches: 'Help'
});

bot.dialog('Greeting', function(session) {
  // parent(session);
  session.endDialog();
}).triggerAction({
  matches: 'Greeting'
});

bot.dialog('Profile', [
  function(session, args) {
    // Save previous state (create on first call)
    session.dialogData.index = (args.index === undefined) ? 0 : args.index;
    session.dialogData.form = (args.form === undefined) ? 0 : args.form;

    // Prompt user for next field
    builder.Prompts.choice(session, questions[session.dialogData.index].question,
      questions[session.dialogData.index].prompt, {
        listStyle: builder.ListStyle.button
      });
  },
  function(session, results) {
    // Save users reply
    var field = questions[session.dialogData.index].field;
    session.dialogData.index = session.dialogData.index + 1;

    // Check for end of form
    if (session.dialogData.index >= questions.length) {
    	console.log(session.dialogData.index);
      // Return completed form
      session.userData.answers = session.dialogData.form;
      session.endDialogWithResult({
        response: session.dialogData.form
      });
    } else {
      // Next field
      session.replaceDialog('Profile', session.dialogData);
    }
  }
]).triggerAction({
  matches: 'Profile'
});

// JS -> PYTHON code
// https://gist.github.com/cowboy/3427148

var parent = function(session) {
  var spawn = require('child_process').spawn;
  var child = spawn('py', ['python-scripts/res.py']);
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

var questions = [{
    question: "How long do you hold a stock?",
    prompt: [
      "Less than 1 year",
      "1 to 2 years",
      "2 to 3 years",
      "3 to 4 years",
      "4 to 5 years",
      "More than 5 years"
    ]
  },
  {
    question: "Which of the following have you owned before or own now?",
    prompt: [
      "N/A",
      "Time deposit or money market funds",
      "Bonds or bond mutual funds",
      "Stock mutual funds",
      "Individual stocks",
      "Leveraged funds"
    ]
  },
  {
    question: "Which best describes your experience of investment?",
    prompt: [
      "None",
      "None beyond bank savings accounts",
      "Some investment experience (mutual funds or individual shares)",
      "Experienced with a portfolio managed by an advisor",
      "Experienced and manage my own portfolio",
      "Buy AMD"
    ]
  },
  {
    question: "What is your prime objective with investment?",
    prompt: [
      "Education of your children",
      "Savings",
      "Capital growth and returns",
      "Retirement",
      "My legacy",
      "Yacht"
    ]
  },
  {
    question: "What percentage of your total savings are invested?",
    prompt: [
      "<10%",
      "10-20%",
      "20-30%",
      "30-40%",
      "40-99%",
      "100%"
    ]
  },
  {
    question: "If you were to invest all your savings into only one of the five investments below, which would you choose?\nChoice             |  Worst Year  |  Average Year  |  Best Year",
    prompt: [
      "Investment A   |  4 %              |   6 %                |  8 %",
      "Investment B   |  2 %              |   8 %                |  14 %",
      "Investment C   | -5 %              |   10 %               |  20 %",
      "Investment D   | -15 %             |   12 %               |  25 %",
      "Investment E   | -20 %             |   15 %               |  30 %",
      "Investment F   | -80 %             |   50 %               |  150 %"
    ]
  },
  {
    question: "What sport would you most like to participate in?",
    prompt: [
      "Baseball",
      "Soccer",
      "Skiing",
      "Rock Climbing",
      "Skydiving",
      "Wingsuit Flying"
    ]
  },
  {
    question: "Which country would you be least likely to visit?",
    prompt: [
      "Venezuela",
      "Mexico",
      "Russia",
      "The United Kingdom",
      "Germany",
      "Iceland"
    ]
  },
  {
    question: "How many bones have you broken?",
    prompt: [
      "0",
      "1-2",
      "3-5",
      "6-9",
      "10-14",
      "15+"
    ]
  },
  {
    question: "Which of these describes you most accurately?",
    prompt: [
      "Cross the street only at crosswalks",
      "Cross the street near crosswalks",
      "Cross the street anywhere if you don’t see cars",
      "Cross the street anywhere if there are no cars in your path",
      "Cross the street anywhere if the cars are moving slowly or have room to stop",
      "Cross the street anywhere, no matter what"
    ]
  }
];
