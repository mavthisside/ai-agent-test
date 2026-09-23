Take-Home Assignment for Customer Support Agent AI

A customer support agent made for the Aster & Row take-home assignment.

The agent utilizes the provided knowledge base to answer queries about policies and products, searches orders by their order ID, maintains context in the conversation, and does not guess when there is no sufficient information.

# Features
-Answers questions about policies and products based on the -local knowledge base
-Semantically and based on keywords retrieves information
-Utilizes active and official documents on policies
-Maintains context through multiple questions
-Searches orders by their order ID
-Detects the order ID in user messages
-Prompts for order ID when needed
-Secures customer and internal information
-Provides the source of answers to policy questions
-Deals with contradictions between official sources
-Does not react to instructions inside retrieved documents
-Does not provide answers without sufficient information
-Web interface
-Tests and evaluation cases

## The mechanism behind it
Initially, the system analyzes the user's request and finds out whether it is a policy/support request or an order request.

In case of policy requests, the agent will perform a search in the local knowledge base and generate the response basing on the gathered information.

In case of an order request, it utilizes the order lookup feature rather than trying to guess the order status.

In case the answer is based on the knowledge base, the source is indicated. In case of lack of relevant information, the system won't generate an answer.

## Project structure
- ai-agent-test/
- data/
- evaluation/
- knowledge-base/
- src/
- tests/
- web/
- BUG_DIARY.md
- debug_retrieval.py
- debug_trailplus.py
- test_agent.py
- web_server.py

## Setup
The project uses Python.

I used Python 3.13.9 while developing and testing the project.

After cloning the repository, open a terminal in the project folder and install the required package:

pip install sentence-transformers

The sentence-transformers package is used for semantic retrieval.

On the first run, the sentence-transformer model may be downloaded from Hugging Face. An API key is not required for the basic setup.

## Running the tests
Run:

python test_agent.py

The tests cover different parts of the agent, including retrieval, order handling, conversation context, privacy, prompt-injection handling, and cases where the agent should not answer.

## Running the web interface
Start the server with:

python web_server.py

Then open:

http://127.0.0.1:8000

The web interface can be used to send questions to the agent and check the responses.

## Example questions 
Questions like the following could be asked:

What is the usual period for return?
What is the period for return for TrailPlus customers?
How long do I have time to notify about any damaged items?
Does Aster & Row deliver to other countries?
Who is the CEO of Aster & Row?

The last one is particularly good to test the agent's abstinence behavior since the provided KB does not have information about that person.

## Retrieval and grounding
The knowledge base includes not only up-to-date but also old, internal, and contradictory documents.

The retriever removes the inappropriate documents and prefers the official sources.

In my tests, I faced the problem of the retrieval of unrelated documents by an unrelated question due to the vector search. It returned the closest matches although their relevance was low.

I implemented a feature which makes the retrieval remove low-relevance matches. If there is no relevant result, the agent can refuse giving any answer.

For instance:
Who is the CEO of Aster & Row?

The agent said it could not find any reliable information after the modification of the retriever.

## Testing
I tested the agent with both normal support questions and questions outside the supplied knowledge base.

Some of the cases tested were:

Standard return window
TrailPlus return window
Damaged item reporting
International shipping
Follow-up questions
Unknown company information
Prompt-injection attempts

The tested support questions returned the relevant policy information and associated source.

For unsupported questions, I also checked that the agent does not use an unrelated retrieved document to produce an answer.

## Evaluation

The final evaluation passed 14 out of 15 provided evaluation cases.

The only failing case was `unsupported-country`, where the agent did not retrieve `06-international-shipping.md` as expected.

## Known limitations

- The order lookup data is mock data provided for the assignment.
- The knowledge base is local and limited to the supplied documents.
- The relevance threshold is fixed rather than learned automatically.
- The system does not perform actions such as issuing refunds or cancelling orders.
- The first run may take longer because the       sentence-transformer model needs to be downloaded.
- Retrieval quality can still vary for very short or unusual queries.

## Bug diary
Issues that were discovered during development can be found in the BUG_DIARY.md file.

One of the major issues that I discovered was associated with retrieval. Even though the question was irrelevant, it was possible to retrieve irrelevant documents since the retriever would provide only top-ranked results.

The reason for this problem was the fact that there was no minimum relevance threshold after the semantic search.

I resolved this problem by implementing a minimum relevance threshold. Any results that have a lower relevance threshold will be ignored by the agent to prevent it from returning an answer with not enough useful information.

I tested my solution on an irrelevant question about company information.

## Notes
This project has been implemented locally as a solution to the take-home assignment for Aster & Row AI agent.

The primary goal was to ensure that the implementation remained compact and easy to test while addressing retrieval quality, groundedness, order search, conversational history, and unsupported queries.