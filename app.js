/*-----------------------------------------------------------------------------
A simple echo bot for the Microsoft Bot Framework.
-----------------------------------------------------------------------------*/
// This loads the environment variables from the .env file
// #ifdef LOCAL
// require('dotenv-extended').load();
// #endif

var restify = require('restify');
var builder = require('botbuilder');

// Setup Restify Server
var server = restify.createServer();
server.listen(process.env.port || process.env.PORT || 3978, function () {
   console.log('%s listening to %s', server.name, server.url);
});

// Create chat connector for communicating with the Bot Framework Service
var connector = new builder.ChatConnector({
    appId: process.env.MicrosoftAppId,
    appPassword: process.env.MicrosoftAppPassword,
    stateEndpoint: process.env.BotStateEndpoint,
    openIdMetadata: process.env.BotOpenIdMetadata
});

// #ifdef DEBUG
// console.log(process.env.MICROSOFT_APP_ID);
// console.log(process.env.MICROSOFT_APP_PASSWORD);
// console.log(process.env.BotStateEndpoint);
// console.log(process.env.BotOpenIdMetadata);
// #endif

// Listen for messages from users
server.post('/api/messages', connector.listen());

/*----------------------------------------------------------------------------------------
* Bot Storage: This is a great spot to register the private state storage for your bot.
* We provide adapters for Azure Table, CosmosDb, SQL Azure, or you can implement your own!
* For samples and documentation, see: https://github.com/Microsoft/BotBuilder-Azure
* ---------------------------------------------------------------------------------------- */

// Create your bot with a function to receive messages from the user
var bot = new builder.UniversalBot(connector, function (session) {
    session.send('Sorry, I did not understand \'%s\'. Type \'help\' if you need assistance.', session.message.text);
});

// Make sure you add code to validate these fields
var luisAppId = process.env.LuisAppId;
var luisAPIKey = process.env.LuisAPIKey;
var luisAPIHostName = process.env.LuisAPIHostName || 'westus.api.cognitive.microsoft.com';
// #ifdef LOCAL
// const LuisModelUrl = process.env.LUIS_MODEL_URL;
// #else
const LuisModelUrl = 'https://' + luisAPIHostName + '/luis/v0/application?id=' + luisAppId + '&subscription-key=' + luisAPIKey;
// #endif

// #ifdef DEBUG
// console.log(process.env.L);
// console.log(process.env.LuisAPIKey);
// console.log(process.env.LuisAPIHostName);
// #endif

// Main dialog with LUIS
var recognizer = new builder.LuisRecognizer("https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/99e54023-bf56-4417-8311-fa5eb2d7245e?subscription-key=a659eee201024a6d92b6cf9a2973374a&timezoneOffset=0&verbose=true&spellCheck=true&q");
bot.recognizer(recognizer);

bot.dialog('Help', function (session) {
    session.endDialog('Hi! Try asking me things like \'search hotels in Seattle\', \'search hotels near LAX airport\' or \'show me the reviews of The Bot Resort\'');
}).triggerAction({
    matches: 'Help'
});

bot.dialog('Greeting', function (session) {
  session.endDialog('Hi! Welcome to Szechuantech');
}).triggerAction({
  matches: 'Greeting'
});
