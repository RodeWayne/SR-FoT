explain_prompt = """You are a knowledgeable scholar. Below is a question with corresponding options and context. Please read and understand the question carefully, explain the meaning of the question, and combine the options and context to explain what information is needed to answer this question. Please note that you cannot directly answer this question.
Question: Is the following trait inherited or acquired?
Katy plays soccer.
Options: ['inherited','acquired']
Context: Hint: Playing soccer takes practice.
Explanation: The question is asking playing soccer is a inherited or acquired trait. To answer the question, we need to know whether the characteristics of playing football, such as taking practice, are inherited or acquired.

Question: Which figure of speech is used in this text?
Lindsey, I've told you a million times: you need to dry the dishes before you put them away.
Options: ['hyperbole', 'paradox']
Context: 
Explanation: The question is asking which figure of speech is used in given text. To answer the question, we need to know the characteristics of each figure of speech in the options and the expression method of the text.

Question: {ori_question}
Options: {options}
Context: {context}
Explanation: """

premise_prompt = """From the perspective of the syllogism, please propose a major premise for the question. Note that the premise you propose should be correct and relevant to the options or context. If the context is empty, please ignore it.
Here are some examples:
Question: Which phrase has a more positive connotation?
Options: ['a cowardly leader','a prudent leader']
Context: 
Major Premise: People who exhibit prudence are generally perceived more positively.

Question: Is the following trait inherited or acquired?
Katy plays soccer.
Options: ['inherited','acquired']
Context: Hint: Playing soccer takes practice.
Major Premise: traits that require practice are usually acquired.

Question: Which figure of speech is used in this text?
Lindsey, I've told you a million times: you need to dry the dishes before you put them away.
Options: ['hyperbole', 'paradox']
Context: 
Major Premise: Exaggerating the characteristics or degree of things to emphasize the effect of expression is hyperbole, expressing a self contradictory or illogical viewpoint or statement is a paradox.

Question: Which word would you find on a dictionary page with the following guide words?
scream - slide
Options: ['suitcase', 'shallow']
Context:
Major Premise: Words on a dictionary page are lexicographically larger than the first guide word and smaller than the second guide word

Question: Does this passage describe the weather or the climate?
There was rain and sleet in Sioux Falls, South Dakota, last weekend.
Options: ['weather', 'climate']
Context:
Major Premise: Weather refers to the short-term atmospheric conditions in a specific location, while climate refers to the long-term patterns of weather in a region.

Here is your task:
Question: {ori_question}
Options: {options}
Context: {context}
Major Premise: """

check_prompt = """Please think step by step to determine whether the following sentence is correct. If it is correct, output "Yes", otherwise output "No": """

problem_prompt = """From the perspective of the syllogism, please ask a minor premise question for the given question. Note that the question you ask should be relevant to the major premise.
Here are some examples:
Given Question: Which phrase has a more positive connotation?
Context: 
Major Premise: People who exhibit prudence are generally perceived more positively.
Minor Premise Question: Which phrase is related to prudunce?

Given Question: Is the following trait inherited or acquired?
Katy plays soccer.
Context: Hint: Playing soccer takes practice. 
Major Premise: traits that require practice are usually acquired.
Minor Premise Question: Is playing soccer a trait that require practice?

Given Question: Which figure of speech is used in this text?
Lindsey, I've told you a million times: you need to dry the dishes before you put them away.
Context: 
Major Premise: Exaggerating the characteristics or degree of things to emphasize the effect of expression is hyperbole, expressing a self contradictory or illogical viewpoint or statement is a paradox.
Minor Premise Question: What's special about the context?

Given Question: Which word would you find on a dictionary page with the following guide words?
scream - slide
Context: 
Major Premise: Words on a dictionary page are lexicographically larger than the first guide word and smaller than the second guide word
Minor Premise Question: What is the result of alphabetical sorting of the options' words and guide words?

Given Question: Does this passage describe the weather or the climate?
There was rain and sleet in Sioux Falls, South Dakota, last weekend.
Context: 
Major Premise: Weather refers to the short-term atmospheric conditions in a specific location, while climate refers to the long-term patterns of weather in a region.
Minor Premise Question: Does the passage describe the short-term atmospheric conditions in a specific location or the long-term patterns of weather in a region?

Here is your task:
Given Question: {ori_question}
Context: {context}
Major Premise: {major}
Minor Premise Question: """

answer_prompt = """Please refer to the options or the context to answer the question completely. If there is no context provided, only refer to the options to answer the question. If you can't answer the question based on context and options, please answer based on your own knowledge.
Here are some examples: 
Question: Which phrase has a more positive connotation?
Options: ['a cowardly leader','a prudent leader']
Context:
Answer: 'a prudent leader' is related to prudunce.

Question: Is playing soccer a trait that require practice?
Options: ['inherited','acquired']
Context: Hint: Playing soccer takes practice.
Katy plays soccer.
Answer: Playing soccer is a trait that require practice.

Question: What's special about the context?
Options: ['hyperbole', 'paradox']
Context: Lindsey, I've told you a million times: you need to dry the dishes before you put them away.
Answer: The context exaggerates the degree of the thing.

Question: What is the result of alphabetical sorting of the options' words and guide words?
Options: ['suitcase', 'shallow']
Context: scream - slide
Answer: The result of alphabetical sorting of the words is: scream - shallow - slide - suitcase. 

Question: Does the passage describe the short-term atmospheric conditions in a specific location or the long-term patterns of weather in a region?
Options: ['weather', 'climate']
Context: There was rain and sleet in Sioux Falls, South Dakota, last weekend.
Answer: The passage describes the short-term atmospheric conditions in a specific location.

Question: {minor_question}
Options: {options}
Context: {context}
Answer: """


final_prompt = """From the perspective of the syllogism, please according to the major premise and minor premise, choose an answer that best fits the question from the options.
Here are some examples:
Major Premise: People who exhibit prudence are generally perceived more positively.
Minor Premise: 'a prudent leader' is related to prudunce.
Question: Which phrase has a more positive connotation?
Options: ['a cowardly leader','a prudent leader']
Answer: The answer is 'a prudent leader'. The reasoning process of syllogism is as follows: Since People who exhibit prudence are generally perceived more positively, and 'a prudent leader' is related to prudunce, it can be concluded that 'a prudent leader' has a more positive connotation.

Major Premise: Traits that require practice are usually acquired.
Minor Premise: Playing soccer is a trait that require practice.
Question: Is the following trait inherited or acquired?
Katy plays soccer.
Options: ['inherited','acquired']
Answer: The answer is 'acquired'. The reasoning process of syllogism is as follows: Since traits that require practice are usually acquired, and playing soccer is a trait that require practice, it can be concluded that playing soccer is acquired.

Major Premise: Exaggerating the characteristics or degree of things to emphasize the effect of expression is hyperbole, expressing a self contradictory or illogical viewpoint or statement is a paradox.
Minor Premise: The context exaggerates the degree of the thing.
Question: Which figure of speech is used in this text?
Lindsey, I've told you a million times: you need to dry the dishes before you put them away.
Options: ['hyperbole', 'paradox']
Answer: The answer is 'hyperbole'. The reasoning process of syllogism is as follows: Since exaggerating the characteristics or degree of things to emphasize the effect of expression is hyperbole while expressing a self contradictory or illogical viewpoint or statement is a paradox, and the context exaggerates the degree of the thing, it can be concluded that hyperbole is used in the text.

Major Premise: Words on a dictionary page are between guide words in alphabetical order.
Minor Premise: The result of alphabetical sorting of the words is: scream - shallow - slide - suitcase. 
Question: Which word would you find on a dictionary page with the following guide words?
scream - slide
Options: ['suitcase', 'shallow']
Answer: The answer is 'shallow'. The reasoning process of syllogism is as follows: Since words on a dictionary page are between guide words in alphabetical order, and the result of alphabetical sorting of the words is: scream - shallow - slide - suitcase, it can be concluded that 'shallow' would be found on a dictionary page with the guide words scream-slide.

Major Premise: Weather refers to the short-term atmospheric conditions in a specific location, while climate refers to the long-term patterns of weather in a region.
Minor Premise: The passage describes the short-term atmospheric conditions in a specific location.
Question: Does this passage describe the weather or the climate?
There was rain and sleet in Sioux Falls, South Dakota, last weekend.
Options: ['weather', 'climate']
Answer: The answer is 'weather'. The reasoning process of syllogism is as follows: Since Weather refers to the short-term atmospheric conditions in a specific location, while climate refers to the long-term patterns of weather in a region, and the passage describes the short-term atmospheric conditions in Sioux Falls, South Dakota, last weekend, it can be concluded that the passage describes the weather.

Here is your task:
Major Premise: {major}
Minor Premise: {minor}
Question: {ori_question}
Options: {options}
Answer: """


only_final_prompt = """From the perspective of the syllogism, please according to the major premise and minor premise, choose an answer that best fits the question from the options.
Here are some examples:
Question: Which phrase has a more positive connotation?
Options: ['a cowardly leader','a prudent leader']
Major Premise: People who exhibit prudence are generally perceived more positively.
Minor Premise: 'a prudent leader' is related to prudunce.
Answer: The answer is 'a prudent leader'. The reasoning process of syllogism is as follows: Since People who exhibit prudence are generally perceived more positively, and 'a prudent leader' is related to prudunce, it can be concluded that 'a prudent leader' has a more positive connotation.

Question: Is the following trait inherited or acquired?
Katy plays soccer.
Options: ['inherited','acquired']
Major Premise: Traits that require practice are usually acquired.
Minor Premise: Playing soccer is a trait that require practice.
Answer: The answer is 'acquired'. The reasoning process of syllogism is as follows: Since traits that require practice are usually acquired, and playing soccer is a trait that require practice, it can be concluded that playing soccer is acquired.

Question: Which figure of speech is used in this text?
Lindsey, I've told you a million times: you need to dry the dishes before you put them away.
Options: ['hyperbole', 'paradox']
Major Premise: Exaggerating the characteristics or degree of things to emphasize the effect of expression is hyperbole, expressing a self contradictory or illogical viewpoint or statement is a paradox.
Minor Premise: The context exaggerates the degree of the thing.
Answer: The answer is 'hyperbole'. The reasoning process of syllogism is as follows: Since exaggerating the characteristics or degree of things to emphasize the effect of expression is hyperbole while expressing a self contradictory or illogical viewpoint or statement is a paradox, and the context exaggerates the degree of the thing, it can be concluded that hyperbole is used in the text.

Question: Which word would you find on a dictionary page with the following guide words?
scream - slide
Options: ['suitcase', 'shallow']
Major Premise: Words on a dictionary page are between guide words in alphabetical order.
Minor Premise: The result of alphabetical sorting of the words is: scream - shallow - slide - suitcase. 
Answer: The answer is 'shallow'. The reasoning process of syllogism is as follows: Since words on a dictionary page are between guide words in alphabetical order, and the result of alphabetical sorting of the words is: scream - shallow - slide - suitcase, it can be concluded that 'shallow' would be found on a dictionary page with the guide words scream-slide.

Question: Does this passage describe the weather or the climate?
There was rain and sleet in Sioux Falls, South Dakota, last weekend.
Options: ['weather', 'climate']
Major Premise: Weather refers to the short-term atmospheric conditions in a specific location, while climate refers to the long-term patterns of weather in a region.
Minor Premise: The passage describes the short-term atmospheric conditions in a specific location.
Answer: The answer is 'weather'. The reasoning process of syllogism is as follows: Since Weather refers to the short-term atmospheric conditions in a specific location, while climate refers to the long-term patterns of weather in a region, and the passage describes the short-term atmospheric conditions in Sioux Falls, South Dakota, last weekend, it can be concluded that the passage describes the weather.

Here is your task:
Question: {ori_question}
Options: {options}
"""