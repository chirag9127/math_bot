# Math Bot
Math Bot is a bot for helping students prepare for SAT Math. This bot powers SAT Buddy (https://www.facebook.com/SATBuddy/)

The bot allows students to:
- Practice questions and tests
- Learn a Math concept by watching a relevant video
- Get a question solved by the bot
- Obtain analytics and graphs on student's performance

The bot is deployed on Heroku and is currently available on Facebook Messenger. 

Our main objective was to build a working prototype for the hackathon. Hence, we used external APIs wherever possible. The following are the different components of the bot. 
1. Scraper:
2. Query handler: 
3. Intent detection:
4. Question Solver:
5. Spell corrector:
6. Video Searcher:
7. Analytics on user performance:

## System Architecture
![alt text](https://github.com/chirag9127/math_bot/blob/master/SystemArchitecture.jpeg)

### Analytics
Analytics queries the database to get diagnostics like topic wise score, questions answered correctly versus questiona attempted over the last week/month/since beginning.
Matplotlib is used to plot the results for each sender.

### Database
An Amazon RDS instance is used to store the answers provided by a sender. There are tables for :
- questions - which include id, question text
- answers - question_id, answer
- answers provided by user - This table is used for generating the analytical reports

### API's used
All the apis intereact with the messenger bot. The user queries are interpreted by the messenger bot and the relevant apis are called.
- api.ai -
- wolfram api - https://products.wolframalpha.com/api/. This is used to provide graphical solution to mathematical queries.
  Wolfram api has solutions to a wide variety of topics covered and the soltuions to a query are sent as a list of gifs.
  This is sent to the messenger bot.
- bing spell checker - this is used mainly in cases where the messenger bot is unable to understand user queries. For eg, when   the user queries contain a lot of spelling mistakes that is hard for api.ai to interpret. In this case, the bing spell         checker returns a list of tuples that contain the position of the starting letter of the misspelled word, along with the
  corrected word. These are constructed back to a complete sentence.
- you tube search api - used to search videos for use queries. 

### ML model - Deep Relevance Model
- TO be filled

### Data set generation
- scapped various SAT prep sites to get questions and answers
- conducted ui testing with a number of initial users to get the test data for api.ai. These mainly include queries that
  users input to practise questions, take diagnostic test, get graphs of scores, search videos on relevant topics and 
  get solutions to various 
  mathematical problems

