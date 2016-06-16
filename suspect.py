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
    duplicates = [random.randint(0, 3) for x in xrange(2)]
    nationalities = ['American', 'Filipino', 'Chinese', 'German']
    jobs = ['Butcher', 'Police', 'Doctor', 'Salesman']
    ages = [random.randint(18, 80) for x in xrange(4)]
    heights = [random.uniform(3, 7) for x in xrange(4)]

    for i, j in enumerate(duplicates):
        suspects[i][x] = suspects[0][x]

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
