class util_rc:
    def __init__(self, modeltype, choice, amt1, prob1, amt2, prob2):
        it = iter([choice, amt1, prob1, amt2, prob2])
        the_len = len(next(it))
        if not all(len(l) == the_len for l in it):
            raise ValueError('all vectors must have the same length')

        if not isinstance(modeltype, str):
            raise TypeError('modeltype must be a string')
        elif modeltype != "E" and modeltype != "R" and modeltype != "W" and modeltype != "H":
            raise Exception("modeltype must be E for expected utility theory, R for risk-return, W for weber, "
                            "or H for hyperbolic")
        else:
            self.model_type = modeltype

        if not all([x == 0 or x == 1 for x in choice]):
            raise Exception("choice must only consists of 0 and 1 where 1 is choosing option 1 and 0 is choosing "
                            "option2")
        else:
            self.choice = choice

        if any([x <= 0 for x in amt1]) or any([x <= 0 for x in amt2]):
            raise Exception("amounts must be positive")
        elif len(amt1) < 3 or len(amt2) < 3:
            raise Exception("must have at least 3 observations")
        else:
            self.amt1 = amt1
            self.amt2 = amt2

        if any([x < 0 or x > 1 for x in prob1]) or any([x < 0 or x >1 for x in prob2]):
            raise Exception("probabilities must be between 0 and 1 (inclusive)")
        else:
            self.prob2 = prob2
            self.prob1 = prob1