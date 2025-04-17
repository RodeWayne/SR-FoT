explain_prompt = """You are a knowledgeable scholar. Below is a question with corresponding context. Please read and understand the question carefully, explain the meaning of the question, and find what information in the context is needed to answer this question. Please note that the information you find must be from the context, and you cannot directly answer this question and assume some information does not appear in the context.
Question: Are more people today related to Genghis Khan than Julius Caesar?
Context: 1.Julius Caesar had three children, while Genghis Khan had sixteen.
2.Modern geneticists found that approximately 1 in 200 men today carry DNA traceable to Genghis Khan.
Explanation: The question is asking for a comparative analysis of the number of living descendants of two historical figures, Genghis Khan and Julius Caesar. Specifically, it seeks to determine whether more people alive today are genetically related to Genghis Khan than to Julius Caesar. To answer whether more people today are related to Genghis Khan than Julius Caesar, one would need to compare the known genetic influence and number of descendants of each.

Question: Would Taylor Swift refer to Snoopy as oppa?
Context: 1.Oppa is a Korean word used by women to address a man who is 10 or more years older than her.
2.Snoopy is 47 years old.
3.Taylor Swift is 30 years old.
Explanation: The question is asking whether Taylor Swift would use the Korean term "oppa" when referring to Snoopy. "Oppa" is used by women to address a man who is at least 10 years older than them. To answer this, one needs to compare the ages of Taylor Swift and Snoopy. Since Snoopy is 47 years old and Taylor Swift is 30 years old, there is a 17-year age difference, which meets the requirement for using the term "oppa."

Question: {question}
Context: {context}
Explanation: """

major_prompt = """From the perspective of the syllogism, please propose a major premise for the question according to the context and the explanation. In a syllogism, the major premise is a general statement or a universal truth. Note that the major premise must be found or supported in the context and as much as possible related to the question. 
Question: Are more people today related to Genghis Khan than Julius Caesar?
Context: 1.Julius Caesar had three children, while Genghis Khan had sixteen.
2.Modern geneticists found that approximately 1 in 200 men today carry DNA traceable to Genghis Khan.
Explanation: The question is asking for a comparative analysis of the number of living descendants of two historical figures, Genghis Khan and Julius Caesar. Specifically, it seeks to determine whether more people alive today are genetically related to Genghis Khan than to Julius Caesar. To answer whether more people today are related to Genghis Khan than Julius Caesar, one would need to compare the known genetic influence and number of descendants of each.
Major Premise: Historical figures with more children and a wider geographical influence are more likely to have a larger number of living descendants today.

Question: Would Taylor Swift refer to Snoopy as oppa?
Context: 1.Oppa is a Korean word used by women to address a man who is 10 or more years older than her.
2.Snoopy is 47 years old.
3.Taylor Swift is 30 years old.
Explanation: The question is asking whether Taylor Swift would use the Korean term "oppa" when referring to Snoopy. "Oppa" is used by women to address a man who is at least 10 years older than them. To answer this, one needs to compare the ages of Taylor Swift and Snoopy. Since Snoopy is 47 years old and Taylor Swift is 30 years old, there is a 17-year age difference, which meets the requirement for using the term "oppa."
Major Premise: Women refer to men who are at least 10 years older than them as "oppa" in Korean culture.

Question: {question}
Context: {context}
Explanation: {explanation}
Major Premise: """

problem_prompt = """From the perspective of the syllogism, please ask a minor premise question for the given question. The minor premise question you ask should be as relevant as possible to the given question.
Question: Are more people today related to Genghis Khan than Julius Caesar? 
Context: 1.Julius Caesar had three children, while Genghis Khan had sixteen.
2.Modern geneticists found that approximately 1 in 200 men today carry DNA traceable to Genghis Khan.
Major Premise: Historical figures with more children and a wider geographical influence are more likely to have a larger number of living descendants today.
Minor Premise Question: Did Genghis Khan have more children and a wider geographical influence than Julius Caesar?

Question: Would Taylor Swift refer to Snoopy as oppa?
Context: 1.Oppa is a Korean word used by women to address a man who is 10 or more years older than her.
2.Snoopy is 47 years old.
3.Taylor Swift is 30 years old.
Major Premise: Women refer to men who are at least 10 years older than them as "oppa" in Korean culture.
Minor Premise Question: Is Snoopy at least 10 years older than Taylor Swift?

Question: {question}
Context: {context}
Major Premise: {major}
Minor Premise Question: """

minor_prompt = """Please according to the context, think step by step to answer the question. Note that You must think and answer only based on the context.
Question: Did Genghis Khan have more children and a wider geographical influence than Julius Caesar?
Context: 1.Julius Caesar had three children, while Genghis Khan had sixteen.
2.Modern geneticists found that approximately 1 in 200 men today carry DNA traceable to Genghis Khan.
Answer: Genghis Khan had more children and a wider geographical influence than Julius Caesar.
1.Genghis Khan had sixteen children, whereas Julius Caesar had three children.
2.Modern geneticists found that approximately 1 in 200 men today carry DNA traceable to Genghis Khan, indicating a wide geographical influence through his descendants.

Question: Is Snoopy at least 10 years older than Taylor Swift?
Context: 1.Oppa is a Korean word used by women to address a man who is 10 or more years older than her.
2.Snoopy is 47 years old.
3.Taylor Swift is 30 years old.
Answer: Snoopy is at least 10 years older than Taylor Swift.
1.Snoopy is 47 years old.
2.Taylor Swift is 30 years old.
3.Since 47 - 30 = 17, Snoopy is 17 years older than Taylor Swift, which is more than 10 years.

Question: {minor_question}
Context: {context}
Answer: """

final_prompt = """From the perspective of the syllogism, please according to the major premise and minor premise, think step by step to determine whether the answer is 'True' or 'False'. 
Major Premise: Historical figures with more children and a wider geographical influence are more likely to have a larger number of living descendants today.
Minor Premise: Genghis Khan had more children and a wider geographical influence than Julius Caesar.
1.Genghis Khan had sixteen children, whereas Julius Caesar had three children.
2.Modern geneticists found that approximately 1 in 200 men today carry DNA traceable to Genghis Khan, indicating a wide geographical influence through his descendants.
Question: Are more people today related to Genghis Khan than Julius Caesar?
Answer: Given the major premise that historical figures with more children and a wider geographical influence are more likely to have a larger number of living descendants today, and the minor premise that Genghis Khan had more children and a wider geographical influence than Julius Caesar, it follows that more people today are likely related to Genghis Khan than to Julius Caesar. The answer to the question is 'True'.

Major Premise: Women refer to men who are at least 10 years older than them as "oppa" in Korean culture.
Minor Premise: Snoopy is at least 10 years older than Taylor Swift.
1.Snoopy is 47 years old.
2.Taylor Swift is 30 years old.
3.Since 47 - 30 = 17, Snoopy is 17 years older than Taylor Swift, which is more than 10 years.
Question: Would Taylor Swift refer to Snoopy as oppa?
Answer: Given the major premise that women refer to men who are at least 10 years older than them as "oppa" in Korean culture, and the minor premise that Snoopy is at least 10 years older than Taylor Swift, it follows that Taylor Swift would refer to Snoopy as oppa. The answer to the question is 'True'.

Major Premise: {major}
Minor Premise: {minor}
Question: {question}
Answer: """