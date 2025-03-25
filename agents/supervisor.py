from generation import generate_hypothesis
from reflection import reflect_on_hypothesis
from ranking import rank_hypothesis
from evolution import evolve_hypothesis
from proximity import proximity_analysis
from meta_review import meta_review

query=input("Enter your query: ")
generation=generate_hypothesis(query)
print(generation)

reflection=reflect_on_hypothesis(generation)
print(reflection)

ranking=rank_hypothesis(reflection)
print(ranking)

evolution=evolve_hypothesis(reflection,query,ranking)
print(evolution)

proximity=proximity_analysis(evolution)
print(proximity)

meta_review=meta_review(generation, reflection, ranking, evolution, proximity)
print(meta_review)