
prompt = """Let's think step by step. Please based on the context, choose one answer that best fits the question from the options. If the context is not provided, please based on your knowledge, choose one answer that best fits the question from the options.After your answer, please provide your reasoning process. 
Question: Which phrase has a more positive connotation?
Options: ['a cowardly leader','a prudent leader']
Context:
Answer: The answer is 'a prudent leader', reasoning process step by step:
1.The options provided are 'a cowardly leader' and 'a prudent leader'.
2.The word 'cowardly' typically has a negative connotation, implying fearfulness or lack of bravery.
3.The word 'prudent' generally has a positive connotation, suggesting wisdom, carefulness, and good judgment.
4.In the context of leadership, being described as 'prudent' implies that the leader is making well-informed and wise decisions, which is generally seen as a positive trait.
5.On the other hand, being described as 'cowardly' suggests a lack of courage and may indicate weakness in a leadership role, generally viewed as negative.
6.Therefore, based on the context and connotations of the words, 'a prudent leader' has a more positive connotation.

Question: Is the following trait inherited or acquired?
Katy plays soccer.
Options: ['inherited','acquired']
Context: Hint: Playing soccer takes practice.
Answer: The answer is 'acquired', reasoning process step by step:
1.The question asks whether the trait of playing soccer is inherited or acquired.
2.The context provides a hint that playing soccer takes practice, implying that it is a skill that is learned or acquired through practice rather than being inherited.
3.In general, playing sports like soccer requires learning and developing specific skills, coordination, and knowledge of the game through training and practice.
4.Inherited traits are typically ones that are passed down genetically from parents to offspring, such as eye color or certain physical characteristics.
5.Playing soccer is not typically considered an inherited trait, as it is a learned skill that individuals acquire over time.
6.Therefore, based on the context and the knowledge that playing soccer is a skill that takes practice, the trait of playing soccer is acquired.

Question: Which figure of speech is used in this text?
Lindsey, I've told you a million times: you need to dry the dishes before you put them away.
Options: ['hyperbole', 'paradox']
Context:
Answer: The answer is 'hyperbole', reasoning process step by step:
1.The question asks which figure of speech is used in the given text.
2.The text includes the phrase "I've told you a million times," which is an exaggerated statement.
3.Hyperbole is a figure of speech that involves intentional exaggeration for emphasis or dramatic effect.
4.In this case, the phrase "a million times" is an exaggerated statement, as it is not meant to be taken literally but rather to emphasize the repetition of the statement.
5.A paradox, on the other hand, refers to a statement or situation that contradicts itself or seems to be self-contradictory.
6.There is no evident paradox in the given text.
7.Therefore, based on the context and the use of exaggerated language, the figure of speech used in this text is 'hyperbole'.

Question: Which word would you find on a dictionary page with the following guide words?
scream - slide
Options: ['suitcase', 'shallow']
Context:
Answer: The answer is 'shallow',reasoning process step by step:
1.The question asks which word would be found on a dictionary page with the guide words "scream" and "slide".
2.Guide words in a dictionary are typically found at the top of each page and represent the first and last entry words on that page.
3.The guide word "scream" would appear at the top left, and the guide word "slide" would appear at the top right.
4.To find a word that would likely be on the same page as these guide words, we need to look for a word that falls alphabetically between "scream" and "slide".
5.The options provided are 'suitcase' and 'shallow'.
6.Comparing the alphabetical order, 'shallow' comes after 'scream' and before 'slide', while 'suitcase' does not fit between them.
7.Therefore, based on the given options and the alphabetical order, the word that would likely be found on a dictionary page with the guide words "scream" and "slide" is 'shallow'.

Question: Does this passage describe the weather or the climate?
There was rain and sleet in Sioux Falls, South Dakota, last weekend.
Options: ['weather', 'climate']
Context:
Answer: The answer is 'weather', reasoning process step by step:
1.The question asks whether the passage describes the weather or the climate.
2.The passage states that there was rain and sleet in Sioux Falls, South Dakota, last weekend.
3.The mention of rain and sleet refers to specific weather conditions that occurred during a particular time frame, which suggests a short-term and immediate occurrence.
4.Weather refers to the conditions of the atmosphere at a specific time and place, including temperature, precipitation, wind, etc.
5.Climate, on the other hand, refers to the long-term patterns of weather observed in a particular area over a longer period.
6.The passage does not provide information about long-term patterns or averages, but rather describes the specific weather conditions that happened in Sioux Falls during a specific weekend.
7.Therefore, based on the context and the focus on specific weather conditions at a particular time, the passage describes the weather, not the climate.

Question: {question}
Options: {options}
Context: {context}
Answer: """


