# Telegram bot

ChatGPT: Through the integration of OpenAI ChatGPT with Telegram, a sophisticated bot has been developed, empowering users with the capability to seamlessly engage with ChatGPT using the OpenAI API under the hood. 

ChatGPT in your Telegram can be used as a learning project to become familiar with API calls, backend development and database integration. 

Planning to practice more OOP by refactoring the whole project to use classes and objects. Deploying MongoDB in a secure way (in the future, the best way to deploy would be to use cloud database solutions). The next steps will be to use GitHub Actions for CI/CD and deploy everything to the cloud (AWS/GCP). For now, the architecture will be a monolith, with the intention to migrate to Kubernetes microservices later on.

### Architecture
Current implementation is based on flask web application framework with NoSQL database MongoDB (bitnami/mongodb docker image) that stores user's __chat_id__, __usernames__ and __OpenaAI API keys__ for each user.

Tested using ngrok.

### Commands
Telegram bot has the following commands:
- /start
- /auth
- /delete 
- /update_token
- /help
