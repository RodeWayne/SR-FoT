premise_prompt = """Let's think step by step. Please answer the question with "True" or "False" according to the passage. After your answer, please provide your reasoning process. 
Question: can you use oyster card at epsom station?
Passage: Epsom railway station serves the town of Epsom in Surrey. It is located off Waterloo Road and is less than two minutes' walk from the High Street. It is not in the London Oyster card zone unlike Epsom Downs or Tattenham Corner stations. The station building was replaced in 2012/2013 with a new building with apartments above the station (see end of article).
Answer: False. According to the passage, epsom station is not in the London Oyster card zone, so you can not use oyster card at epsom station. So the answer is 'False'.

Question: is it possible to have an online relationship?
Passage: An internet relationship is a relationship between people who have met online, and in many cases know each other only via the Internet . Online relationships are similar in many ways to pen pal relationships. This relationship can be romantic, platonic, or even based on business affairs. An internet relationship (or online relationship) is generally sustained for a certain amount of time before being titled a relationship, just as in-person relationships. The major difference here is that an internet relationship is sustained via computer or online service, and the individuals in the relationship may or may not ever meet each other in person. Otherwise, the term is quite broad and can include relationships based upon text, video, audio, or even virtual character. This relationship can be between people in different regions, different countries, different sides of the world, or even people who reside in the same area but do not communicate in person.
Answer: True. According to the passage, an online relationship can be between people in different regions, different countries, different sides of the world, or even people who reside in the same area but do not communicate in person, so it is possible to have an online relationship. So the answer is 'True'.

Question: {q}
Passage: {p}
Answer: """


