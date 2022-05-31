import random

from generatorApis.genPelevin import generatePelevin as _generatePelevin
from generatorApis.genSber import generateSber as _generateSber
from generatorApis.genSber2 import generateSberLargeText as _generateSberLarge


class TextGeneratorWorker:
    def generateDefault(self, string):
        return self.generate_sberLarge(string)

    def generate_pelevin(self, string):
        resultMaybeList = _generatePelevin(string)
        if type(resultMaybeList) is list:
            random.shuffle(resultMaybeList)
            return string + resultMaybeList[0]
        else:
            return string + resultMaybeList

    def generate_sber(self, string, isUseLargeGpt=True):
        """
        Этот можен отваливаться первые запросов десять, или мб тут кулдаун хз
        С какого-то момента начинает работать без проблем
        """
        result = _generateSber(string, isUseLargeGpt)
        return result

    def generate_sberLarge(self, string):
        result = _generateSberLarge(string)
        return result
