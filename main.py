from tokenizer import tokenize_text
from chain import get_data, generate

SAMPLE = """
The ocean is a vast and restless place, full of mysteries that humans have only begun to understand.
Waves roll across the surface, driven by winds that circle the planet without rest.
Beneath the waves, sunlight fades quickly into a cold and silent darkness.
Creatures live there that have never seen the sun, and some of them produce their own light.
The deep sea is the largest habitat on Earth, yet it remains one of the least explored.
Scientists send submersibles into the abyss, hoping to find new species and new answers.
Every dive brings back something unexpected, a new shape, a new color, a new way of surviving.
The ocean also feeds us, moves our weather, and regulates the temperature of the entire planet.
Without the ocean, the climate as we know it would not exist.
The forest is another world, layered from the shaded floor to the bright and swaying canopy.
Trees compete for light, and the tallest ones cast long shadows over everything below.
Fungi connect the roots of trees underground, forming networks that share water and nutrients.
A single acre of forest can hold thousands of species, most of them small and unnoticed.
Birds nest in the branches, insects crawl through the leaf litter, and deer move quietly between the trunks.
When a tree falls, it opens a gap in the canopy, and sunlight floods the forest floor.
New growth rushes in to fill the space, and the cycle begins again.
Forests store carbon, clean the air, and hold the soil together with their roots.
The city is a different kind of ecosystem, built by people and shaped by their needs.
Streets carry traffic, sidewalks carry pedestrians, and buildings rise in tight clusters.
At night the city glows with electric light, and the noise of the day slowly fades.
Markets open early, offices fill by nine, and restaurants serve food long after dark.
Millions of people live close together, yet each of them moves through the city alone.
Trains, buses, and bicycles carry them from home to work and back again.
The city grows outward and upward at the same time, always changing, always rebuilding.
Old neighborhoods give way to new towers, and the skyline shifts year by year.
The desert is a place of extremes, hot by day and cold by night.
Rain falls rarely, sometimes not for years, and yet life finds a way to persist.
Plants store water in thick leaves and deep roots, and animals sleep through the heat.
Sand dunes move slowly with the wind, reshaping the land one grain at a time.
At dawn the desert is quiet, and the sky turns from black to gold in a few short minutes.
The mountains rise where the earth folds and breaks, pushing rock into the sky.
Snow gathers on the peaks and melts in the spring, feeding rivers far below.
Climbers move slowly upward, measuring each step against the thin and bitter air.
At the summit, the world looks small, and the wind carries no sound but its own.
Time moves differently in these places, measured in seasons and centuries rather than hours.
A river carves its channel over thousands of years, wearing stone into sand.
A glacier advances and retreats, leaving valleys behind when it finally melts.
A volcano builds a new island, and life arrives on it within a few short decades.
The planet is always changing, even when the change is too slow for us to see.
Science is the tool we use to notice these changes and to understand them.
We measure, we test, we question, and we revise what we thought we knew.
Every answer opens a new question, and every discovery reveals a deeper mystery.
Curiosity drives us forward, and doubt keeps us honest.
The universe is larger than we can imagine, and older than we can easily grasp.
Stars are born in clouds of gas and die in brilliant explosions.
Galaxies spin slowly through the dark, held together by gravity and by things we cannot yet explain.
Light from distant stars reaches us after millions of years, carrying news of a time before we existed.
We look up and see the past, and in that light we find clues about the future.
Knowledge grows slowly, one observation at a time, one idea at a time, one person at a time.
And yet, in the end, everything we know is built on questions we were brave enough to ask.
"""

if __name__ == "__main__":
    sentences = tokenize_text(SAMPLE)
    data = get_data(sentences)

    print(f"Text length: {len(SAMPLE)}")
    print("Starters:", data.starts.most_common(5))
    print("After 'the':", data.chain["the"].most_common(5))

    for _ in range(10):
        print(" ".join(generate(data, length=25)))