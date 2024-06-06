from enum import Enum


class PSRFunction(Enum):
    """Enumeration of PSR library function types.

    Parameters
    ----------
    Enum : PSR Function Types
        Partial Sample Regression function types.
    """    
    PREDICT = (0, 'predict')
    MAXFIT = (1, 'maxfit')
    CKT = (2, 'ckt')
    RELEVANCE = (3, 'relevance')
    SIMILARITY = (4, 'similarity')
    INFORMATIVENESS = (5, 'informativeness')
    FIT = (6, 'fit')
    ADJUSTED_FIT = (7, 'adjusted_fit')
    ASYMMETRY = (8, 'asymmetry')
    CO_OCCURENCE = (9, 'co-occurence')
    
    
    def __str__(self):
        return self.value[1]
        
    def __float__(self):
        return float(self.value[0])
    
    def __int__(self):
        return self.value[0]