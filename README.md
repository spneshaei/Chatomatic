# Chatomatic
A very easy to use and performant Python library for developing intelligent chatbots.

Integrate a chatbot in your project easily with **less than 5 lines** of Python code!

## How does Chatomatic work?

1. Define sample questions and answers via CDL (*Chatomatic Definition Language*) which is an easy to read specification, or provide Q&As through **ChatomaticUI**, an easy to use GUI web app, and export a CDL file. Chatomatic accepts YAML files, too.

2. Import Chatomatic in your web API (e.g. Flask) code, and give the path of the CDL file to the initializer.

3. That’s it! Any time a new query arrives, Chatomatic will first look into the Q&As; if it couldn’t find an entry, it will search for the most relevant question in the CDL file, using performant NLP models. It will also cache the result, so the next time, it wouldn’t need to run the Transformer model again, saving resource and time.

Chatomatic will take care of the invalidation of the cache files in case of any change in the Q&As, and other common sources for errors happening in chatbot tools, so you can only focus on your projects and ideas and not worry about how Chatomatic works under the hood.

Also, Chatomatic supports multiple languages at once, out of the box, so you can develop multi-language projects with ease!
