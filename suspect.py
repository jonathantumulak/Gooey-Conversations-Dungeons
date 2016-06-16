import random


class Prisoner(object):
    def __init__(self, age, height, job, nationality, guilty):
        self.age = age
        self.height = height
        self.job = job
        self.nationality = nationality
        self.guilty = guilty


def generateSuspects():
    suspects = [[random.randint(0, 3) for x in xrange(0, 4)] for y in xrange(0, 3)]
    duplicates = []
    nationalities = ['American', 'Filipino', 'Chinese', 'German']
    jobs = ['Butcher', 'Police', 'Doctor', 'Salesman']
    ages = [random.randint(18, 80) for x in xrange(4)]
    heights = [random.uniform(3, 7) for x in xrange(4)]

    duplicate_choices = [x for x in xrange(4)]
    for _ in xrange(3):
        choice = random.choice(duplicate_choices)
        duplicates.append(choice)
        duplicate_choices.remove(choice)

    for i, j in enumerate(duplicates):
        if i < 2:
            print i
            suspects[i+1][j] = suspects[0][j]
        else:
            print i
            suspects[i-1][j] = suspects[0][j]

    prisonerArray = []
    for x, suspect in enumerate(suspects):
        if x == 0:
            prisonerArray.append(Prisoner(
                ages[suspect[0]],
                heights[suspect[1]],
                jobs[suspect[2]],
                nationalities[suspect[3]],
                True
            ))
        else:
            if suspect == suspects[0]:
                suspect[x] = [random.randint(0, 3) for x in xrange(0, 4)]
            else:
                prisonerArray.append(Prisoner(
                    ages[suspect[0]],
                    heights[suspect[1]],
                    jobs[suspect[2]],
                    nationalities[suspect[3]],
                    False
                ))

    random.shuffle(prisonerArray)

    # for prisoner in prisonerArray:
    #     print ""
    #     print prisoner.age
    #     print prisoner.height
    #     print prisoner.job
    #     print prisoner.nationality
    #     print prisoner.guilty
    #     print ""

    return prisonerArray
