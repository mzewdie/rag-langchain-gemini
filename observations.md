1.
I have observed the following in the splitter: 1. The splitter contains in every page the foot note repeatedly. 2. In the first page for example the order is not correct. In the document: "Train the Trainers in Food Safety and Nutrition. Introduction to Nutrition" and in the splitter: Introduction to Nutrition Train the Trainers in Food Safety and Nutrition". That is to observe in many pages. Images are documented as "Illustration : Photo, drawing, clipart �", (Even pages are sometimes are presented not in their right order : to check it) etc.
Summary:
Footer repetition caused by PDF extraction.
Reading order may differ from the visual layout.
Images are not interpreted by text loaders.
Metadata is preserved across chunking.

2.
There was a result in the response, something like "sources of vitamin C  � Fresh fruit especially citrus fruits and berries....". I think for our question "Where is the kitten sleeping?, without storing it first in the database, this is not a right response.
Summary:
Observation: similarity_search() always returns the k nearest documents. It does not determine whether those documents are sufficiently relevant. For robust RAG systems, similarity scores or additional relevance checks are often required to avoid presenting unrelated context to the LLM.
