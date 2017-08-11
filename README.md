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

