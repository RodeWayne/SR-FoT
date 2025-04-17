base_prompt = """Please think step by step to answer the question according to the context. 
Question: Are more people today related to Genghis Khan than Julius Caesar?
Context: 1.Julius Caesar had three children, while Genghis Khan had sixteen.
2.Modern geneticists found that approximately 1 in 200 men today carry DNA traceable to Genghis Khan.
Answer: First, consider the number of offspring each historical figure had: Julius Caesar had three children, while Genghis Khan had sixteen. Modern geneticists have found that approximately 0.5%% of men worldwide carry Genghis Khan's DNA, which suggests a significant number of descendants. Therefore, more people today are likely related to Genghis Khan than Julius Caesar due to his larger number of offspring and the spread of his genetic legacy over time. The answer is 'True'.

Question: Would Taylor Swift refer to Snoopy as oppa?
Context: 1.Oppa is a Korean word used by women to address a man who is 10 or more years older than her.
2.Snoopy is 47 years old.
3.Taylor Swift is 30 years old.
Answer: First, consider the definition of "oppa": it is a Korean term used by women to address a man who is 10 or more years older than her. Next, compare the ages of Taylor Swift and Snoopy: Taylor Swift is 30 years old, and Snoopy is 47 years old. Since Snoopy is indeed more than 10 years older than Taylor Swift, the criteria for using the term "oppa" are met. The answer is 'True'.

Question: {question}
Context: {context}
Answer: """
