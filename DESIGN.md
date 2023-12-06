# Design Document

## Monolithic repository
The first decision I had to make was whether or not to use a monolithic repository or to separate my frontend from my backend. I ended up deciding to use a monolithic repository for several reasons. Firstly, because I was the only developer for this project, it would be easier if I could combine commits of the frontend and backend and push them together. This reduced the effort to hide features behind flags and such. Furthermore, since the system was not being used by anyone and could afford downtime, a monolithic repository made more sense. I did run into some problems when I initially tried to host the frontend on Vercel and the backend on Heroku, although both services allow you to specify a subdirectory from the Github repo you connect to it so everything worked out fine.

## Technical Stack
### Django Rest Framework
The backend was built in Django, which is a web framework in Python. I had previous experience with this and like using it. It has an active community and has been tested on large systems such as the DoorDash platform. Django Rest Framework is a third-party framework that allows you to easily create REST APIs that can be consumed by a frontend.

### React
I used React to build the frontend. React is a way to make UIs using reusable, modular components. It was created and is currently maintained by Facebook. I have used React before and enjoyed using it. It makes creating User Interfaces easier and ensures that your website has a consistent aesthetic throughout all of its pages.

### Redux
Redux is a third-party library used with React and a design approach that allows for a global state. One issue with React is that it can be difficult to store global state for your application. Instead, each component stores its own state and can pass down information to its child components. But if the component hierarchies get very long, it can result in something called "prop-drilling," which is cumbersome and error-prone. For this reason, people invented Redux, which allows you to store a global, immutable state that can be accessed by any component regardless of where it is in the component hierarchy. I wanted to use Redux so that I could store the results of the search results even if the user navigated away to another page.

### NextJS
NextJS is a web framework for React. It comes with additional bells and whistles and makes development quicker. I had never used this technology before, but I wanted to host the frontend on Vercel and there is easy compatibility between the two.

### OpenAI APIs
I consumed OpenAI APIs in the backend to parse the medical note. This required me to open a developer account and spend around $20 in credits. I used the GPT 3.5 Turbo model for all tasks, which, although is not the best model in terms of quality, is very quick.

## Core Components
The project can be broken down into four key components.

### Homepage
The homepage is straightforward. It contains a textbox and button so that people can copy and paste their medical notes. Once the generate recommendations button is pressed, the medical note gets stored in the application's global Redux state. The page redirects the user to the search results page, which calls our backend API to get the proper recommendation result. While it is fetching data, it shows a loading page to the user.

### Note Parser
When the frontend calls the backend to get recommendation results, it provides the backend with the medical note as a plain text object. The note parser component in the backend processes this unstructured medical note to create a structured QueryData object. This QueryData object has fields such as age, sex, type of infection, allergies, and more.

The unstructured medical note is processed using OpenAI APIs. In particular, I use GPT 3.5 Turbo and feed the medical note to it. Then I ask queries to the model, such as "What is the patient's age?". I also include some prompt engineering to ensure I get the output in the format I desire. I recently learned that OpenAI LLMs can now produce JSON, which is how I would implement this component in the future. I ran into some issues early on where the output of the LLM would be slightly different from hardcoded data that appeared later on in the system. For example, it would say the infection was "spontaneous bacterial peritonitis (sbp)." The ending "(sbp)" would not match data that appeared later on in the system.

### Recommendation Engine
Once the note parser produced a QueryData object from the medical note, this QueryData object was passed to the recommendation engine. The recommendation engine would then construct a decision tree for the infection type in question. The decision tree was made up of node objects that could be one of two types. A node could be a decision branch node or a regimen node. All leaf nodes were regimen nodes, and all non-leaf nodes were decision branch nodes. The decision trees would be traversed from the root to a leaf node, taking various branches down the tree according to information stored in QueryData.

### Search results page
Once a regimen leaf node was reached in the decision tree, this data was transformed into a JSON object and sent to the frontend. The frontend then unpacked this object and presented it to the user.
