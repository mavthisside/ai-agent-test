# AI Agent Intern Take-Home

A small, deterministic AI customer-support agent built around retrieval-augmented generation (RAG), policy grounding, order lookup, multi-turn session context, and safe escalation.

## Features

- Retrieval-augmented answers from a local knowledge base
- Hybrid semantic/keyword retrieval
- Policy-aware evidence selection
- Multi-turn conversation context
- Order lookup tool
- Order-ID extraction and clarification
- Customer-data privacy protection
- Source citations in responses
- Handling of conflicting official sources
- Protection against retrieved prompt injection
- Abstention when the knowledge base does not contain enough information
- Deterministic behavior suitable for automated evaluation

## Architecture

```text
User Message
     |
     v
+------------+
|   Router   |
+------------+
     |
     +------------------+
     |                  |
     v                  v
 Policy Query       Order Query
     |                  |
     v                  v
    RAG            Order Lookup
     |                  |
     +--------+---------+
              |
              v
        Grounded Response
              |
              v
       Citation / Handoff