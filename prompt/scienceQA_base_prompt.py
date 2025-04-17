prompt = """Please based on the context, choose one answer that best fits the question from the options. If the context is not provided, please based on your knowledge, choose one answer that best fits the question from the options.
Question: Which phrase has a more positive connotation?
Options: ['a cowardly leader','a prudent leader']
Context:
Answer: a prudent leader

Question: Is the following trait inherited or acquired?
Katy plays soccer.
Options: ['inherited','acquired']
Context: Hint: Playing soccer takes practice.
Answer: acquired

Question: Which figure of speech is used in this text?
Lindsey, I've told you a million times: you need to dry the dishes before you put them away.
Options: ['hyperbole', 'paradox']
Context:
Answer: hyperbole

Question: Which word would you find on a dictionary page with the following guide words?
scream - slide
Options: ['suitcase', 'shallow']
Context:
Answer: shallow

Question: Does this passage describe the weather or the climate?
There was rain and sleet in Sioux Falls, South Dakota, last weekend.
Options: ['weather', 'climate']
Context:
Answer: weather

Question: {question}
Options: {options}
Context: {context}
Answer: """
