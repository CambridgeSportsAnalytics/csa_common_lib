from enum import Enum


class PSRFunction(Enum):
    """Enumeration of PSR library function types.

    Parameters
    ----------
    Enum : PSR Function Types
        Partial Sample Regression function types.
    """    
    PSR = (0, 'psr')
    MAXFIT = (1, 'maxfit')
    GRID = (2, 'grid')
    GRID_SINGULARITY = (3, 'grid_singularity')
    RELEVANCE = (4, 'relevance')
    SIMILARITY = (5, 'similarity')
    INFORMATIVENESS = (6, 'informativeness')
    FIT = (7, 'fit')
    ADJUSTED_FIT = (8, 'adjusted_fit')
    ASYMMETRY = (9, 'asymmetry')
    CO_OCCURENCE = (10, 'co-occurence')
    
    
    def __str__(self):
        return self.value[1]
        
    def __float__(self):
        return float(self.value[0])
    
    def __int__(self):
        return self.value[0]