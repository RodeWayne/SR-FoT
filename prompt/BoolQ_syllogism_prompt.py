explanation_prompt = """You are a knowledgeable scholar. Below is a question with corresponding passage. Please read and understand the question carefully, then explain the meaning of the question.
Question: can you use oyster card at epsom station?
Passage: Epsom railway station serves the town of Epsom in Surrey. It is located off Waterloo Road and is less than two minutes' walk from the High Street. It is not in the London Oyster card zone unlike Epsom Downs or Tattenham Corner stations. The station building was replaced in 2012/2013 with a new building with apartments above the station (see end of article).
Explanation: The question "Can you use an Oyster card at Epsom station?" seeks to determine whether the Oyster card, a contactless payment card used for public transport in London, is accepted for travel at Epsom railway station.

Question: is it possible to have an online relationship?
Passage: An internet relationship is a relationship between people who have met online, and in many cases know each other only via the Internet . Online relationships are similar in many ways to pen pal relationships. This relationship can be romantic, platonic, or even based on business affairs. An internet relationship (or online relationship) is generally sustained for a certain amount of time before being titled a relationship, just as in-person relationships. The major difference here is that an internet relationship is sustained via computer or online service, and the individuals in the relationship may or may not ever meet each other in person. Otherwise, the term is quite broad and can include relationships based upon text, video, audio, or even virtual character. This relationship can be between people in different regions, different countries, different sides of the world, or even people who reside in the same area but do not communicate in person.
Explanation: The question "Is it possible to have an online relationship?" seeks to determine whether it is feasible for people to form and maintain relationships through online means, without necessarily meeting in person.

Question: {q}
Passage: {p}
Explanation: """

premise_prompt = """From the perspective of the syllogism, please propose a major premise for the question according to the passage and the explanation. In a syllogism, the major premise is a general statement or a universal truth. Note that the major premise must be found or supported in the passage. 
Question: can you use oyster card at epsom station?
Passage: Epsom railway station serves the town of Epsom in Surrey. It is located off Waterloo Road and is less than two minutes' walk from the High Street. It is not in the London Oyster card zone unlike Epsom Downs or Tattenham Corner stations. The station building was replaced in 2012/2013 with a new building with apartments above the station (see end of article).
Explanation: The question asks if an Oyster card can be used at Epsom station. The passage states that Epsom station is not in the London Oyster card zone, so the answer can be derived from this information.
Major Premise: Oyster card can be used in the London oyster card zone.

Question: is it possible to have an online relationship?
Passage: An internet relationship is a relationship between people who have met online, and in many cases know each other only via the Internet . Online relationships are similar in many ways to pen pal relationships. This relationship can be romantic, platonic, or even based on business affairs. An internet relationship (or online relationship) is generally sustained for a certain amount of time before being titled a relationship, just as in-person relationships. The major difference here is that an internet relationship is sustained via computer or online service, and the individuals in the relationship may or may not ever meet each other in person. Otherwise, the term is quite broad and can include relationships based upon text, video, audio, or even virtual character. This relationship can be between people in different regions, different countries, different sides of the world, or even people who reside in the same area but do not communicate in person.
Explanation: The question asks if online relationships are possible. The passage explains that online relationships can be romantic, platonic, or business-related and are maintained through digital communication methods, even if the individuals never meet in person. Thus, the information needed to answer the question is that online relationships are indeed possible.
Major Premise: An internet relationship is a relationship between people who have met online.

Question: {q}
Passage: {p}
Explanation: {e}
Major Premise: """

problem_prompt = """From the perspective of the syllogism, please ask a minor premise question for the given question. 
Question: can you use oyster card at epsom station?
Passage: Epsom railway station serves the town of Epsom in Surrey. It is located off Waterloo Road and is less than two minutes' walk from the High Street. It is not in the London Oyster card zone unlike Epsom Downs or Tattenham Corner stations. The station building was replaced in 2012/2013 with a new building with apartments above the station (see end of article).
Major Premise: Oyster card can be used in the London oyster card zone.
Minor Premise Question: Is Epsom station within the London Oyster card zone?

Question: is it possible to have an online relationship?
Passage: An internet relationship is a relationship between people who have met online, and in many cases know each other only via the Internet . Online relationships are similar in many ways to pen pal relationships. This relationship can be romantic, platonic, or even based on business affairs. An internet relationship (or online relationship) is generally sustained for a certain amount of time before being titled a relationship, just as in-person relationships. The major difference here is that an internet relationship is sustained via computer or online service, and the individuals in the relationship may or may not ever meet each other in person. Otherwise, the term is quite broad and can include relationships based upon text, video, audio, or even virtual character. This relationship can be between people in different regions, different countries, different sides of the world, or even people who reside in the same area but do not communicate in person.
Major Premise: An internet relationship is a relationship between people who have met online.
Minor Premise Question: Is it possible for the people to met online?

Question: {q}
Passage: {p}
Major Premise: {major}
Minor Premise Question: """

minor_prompt = """Please answer the question step by step. There may be useful information in the message. If not, please answer based on your own knowledge. 
Question: Is Epsom station within the London Oyster card zone?
Passage: Epsom railway station serves the town of Epsom in Surrey. It is located off Waterloo Road and is less than two minutes' walk from the High Street. It is not in the London Oyster card zone unlike Epsom Downs or Tattenham Corner stations. The station building was replaced in 2012/2013 with a new building with apartments above the station (see end of article).
Answer: Epsom station is not within the London Oyster card zone.
1.Epsom railway station serves the town of Epsom in Surrey.
2.It is less than two minutes' walk from the High Street.
3.The passage explicitly states: "It is not in the London Oyster card zone unlike Epsom Downs or Tattenham Corner stations."

Question: Is it possible for the people to met online?
Passage: An internet relationship is a relationship between people who have met online, and in many cases know each other only via the Internet . Online relationships are similar in many ways to pen pal relationships. This relationship can be romantic, platonic, or even based on business affairs. An internet relationship (or online relationship) is generally sustained for a certain amount of time before being titled a relationship, just as in-person relationships. The major difference here is that an internet relationship is sustained via computer or online service, and the individuals in the relationship may or may not ever meet each other in person. Otherwise, the term is quite broad and can include relationships based upon text, video, audio, or even virtual character. This relationship can be between people in different regions, different countries, different sides of the world, or even people who reside in the same area but do not communicate in person.
Answer: It is possible for the people to meet online.
1.The passage defines an internet relationship as a relationship between people who have met online.
2.It states that these individuals, in many cases, know each other only via the Internet.
3.The relationship can be sustained via computer or online service, and the individuals may or may not ever meet each other in person.
4.The passage also mentions that such relationships can be based on text, video, audio, or virtual character, indicating various ways people can connect online.

Question: {minor_q}
Passage: {p}
Minor Premise: """


final_prompt = """From the perspective of the syllogism, please according to the major premise and minor premise, determine whether the answer to the question is 'True' or 'False'. 
Major Premise: Oyster card can be used in the London oyster card zone.
Minor Premise: Epsom station is not within the London Oyster card zone.
1.Epsom railway station serves the town of Epsom in Surrey.
2.It is less than two minutes' walk from the High Street.
3.The passage explicitly states: "It is not in the London Oyster card zone unlike Epsom Downs or Tattenham Corner stations."
Question: can you use oyster card at epsom station?
Answer: Given that Epsom station is not within the London Oyster card zone and the major premise states that Oyster cards can only be used within this zone, the answer to the question "Can you use an Oyster card at Epsom station?" is 'False'.

Major Premise: An online relationship is a relationship between people who have met online.
Minor Premise: It is possible for the people to meet online.
1.The passage defines an internet relationship as a relationship between people who have met online.
2.It states that these individuals, in many cases, know each other only via the Internet.
3.The relationship can be sustained via computer or online service, and the individuals may or may not ever meet each other in person.
4.The passage also mentions that such relationships can be based on text, video, audio, or virtual character, indicating various ways people can connect online.
Question: is it possible to have an online relationship?
Answer: Given that the definition of an online relationship is based on people meeting online and that it is stated to be possible for people to meet online, the answer to the question "Is it possible to have an online relationship?" is be 'True'.

Major Premise: {major}
Minor Premise: {minor}
Question: {q}
Answer: """

only_final_prompt = """From the perspective of the syllogism, please determine whether the answer to the question is 'True' or 'False'. 
Here are some examples:
Question: can you use oyster card at epsom station?
Major Premise: Oyster card can be used in the London oyster card zone.
Minor Premise: Epsom station is not within the London Oyster card zone.
1.Epsom railway station serves the town of Epsom in Surrey.
2.It is less than two minutes' walk from the High Street.
3.The passage explicitly states: "It is not in the London Oyster card zone unlike Epsom Downs or Tattenham Corner stations."
Answer: Given that Epsom station is not within the London Oyster card zone and the major premise states that Oyster cards can only be used within this zone, the answer to the question "Can you use an Oyster card at Epsom station?" is 'False'.

Question: is it possible to have an online relationship?
Major Premise: An online relationship is a relationship between people who have met online.
Minor Premise: It is possible for the people to meet online.
1.The passage defines an internet relationship as a relationship between people who have met online.
2.It states that these individuals, in many cases, know each other only via the Internet.
3.The relationship can be sustained via computer or online service, and the individuals may or may not ever meet each other in person.
4.The passage also mentions that such relationships can be based on text, video, audio, or virtual character, indicating various ways people can connect online.
Answer: Given that the definition of an online relationship is based on people meeting online and that it is stated to be possible for people to meet online, the answer to the question "Is it possible to have an online relationship?" is be 'True'.

Here is your task:
Question: {q}
"""