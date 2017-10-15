### SzechuanTech RoboAdvisor (STRAT) @ HackGT

SzechuanTech brings professional risk management from BlackRock to individual investors looking to diversify investment portfolios and learn more about investments. Through an easy-to-use chatbot, users can get suggestions to diversify and grow their portfolio, getting quick access to broken-down information about any stock.

## Inspiration

Even in 2017, managing financial securities involves either long and tedious meetings with a financial advisor, cold and impersonal interactions with an algorithm, or a mix of both. We felt that there was an opening in the chat bot marketplace for providing personalized financial data and recommendations to every day users.

## What it does

STRAT acts the user a series of personality-based questions to assess his or her risk profile, using the answers to calculate a number between zero (most risk-averse) and one (least risk-averse). These answers define the profile of the user for interacting with STRAT. Then, on prompt from the user, the bot can either (1) provide information about a specific financial security (e.g. "tell me about apple") or (2) make recommendations that fit the calculated risk profile of the user (e.g. "suggest a stock").

## How we built it

The chat bot was built using the NodeJS implementation of the Microsoft Bot Framework. The bot runs on an Microsoft Azure instance and can be plugged into several different messaging services, such as Slack, Messenger, and Skype (or, more simply, on the Microsoft Bot Emulator). The bot invokes Python scripts on the back-end that fetch data from Blackrock's Aladdin REST API to be used to provide information about financial securities for the users and data for calculations about the risk of each security (so as to make the best recommendation to the user).

## Challenges we ran into

Definitions of the terms on the Aladdin API were few and far between, so we had to do a fair bit of research to determine what metrics were best suited for our purposes. The data from Aladdin, too, was not perfectly matched with our intentions, so we had to do some hacking to get the data and metrics we wanted without making a bajillion HTTP requests. Additionally, our group was much more comfortable to fetch data from Aladdin in Python instead of Node, so we had to use some creative workarounds to call the scripts we wrote from the `app.js` file. This inadvertently led to the Python integration (and thus the entire bot) failing much more than we would have liked. Finally, for the longest time we were running our bot on a purely free instance of Azure, which murdered the performance and responsiveness of our initial protoype. It was only until we set up our bot, with the help of a Microsoft employee, on an instance with a pass for credit that it became functional.

## Accomplishments that we're proud of

This was the first real hackathon for most of the group, so to churn out a project we all found interesting and loved building is something we can tell our parents about. We also built something that we felt filled a need and helped solve a common issue (or at least make valuable steps to do so). Some of us also found that we were able to thrive mentally despite very little (see: none) sleep.

## What we learned

Documentation of a framework or API is nearly as crucial to their effectiveness as how well the technology is actually implemented. A corollary to that, it turns out, is that the more the implementation of a technology deviates from your specific use-case, the more creative you have to get when incorporating said technology into the functionality of your project.

## What's next for STRAT

It would be cool to inegrate the bot with the (unofficial) Robinhood API to allow the user to buy stocks on their Robinhood account after receiving a certain recommendation or quote. The bot could also be much more versatile if it took into account factors other than risk and volatility when making a recommendation (and also ask similar personality questions for those other factors).