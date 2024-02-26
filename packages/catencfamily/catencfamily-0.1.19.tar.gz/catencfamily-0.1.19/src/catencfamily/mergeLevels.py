# Last amended: 25th Feb, 2024

from sklearn.base import BaseEstimator, TransformerMixin



class RareLevelMergerTransformer(BaseEstimator, TransformerMixin):
    """
    Merge levels in multiple features that are below certain 
    thresholds.
    
    """

    def __init__(self):
        # Define two variables that can be passed
        #  on to fit() to decide which levels
        #   per-feature to merge
        self.featurewiseLevels_to_merge = {}
        # And below which threshold
        self.thresholds = {}  # this is in fraction

    # Learn about data
    # Also see: https://stackoverflow.com/a/56791194/3282777
    def fit(self, X, y=None, **kwargs):
        """
        Calls: _learnLevelsBelowThreshold()
        Called by: class object
        
        Parameters
        ----------
        X : pandas DataFrame
        y : Not used in fit method
        kwargs : dictionary. Its keys are column names
                             and values are threshold.
                             Levels which occur below
                             the specified fraction
                             (threshold) are to be
                             merged.

        Returns
        -------
        class object itself

        """
        self._learnLevelsBelowThreshold(X, **kwargs)
        return self
 
    
 # Perform transformation 
    def transform(self, X):
        """
        Calls: _mergeLevels()
        Called by: class object
            
        Parameters
        ----------
        X: Pandas DataFrame to be transformed
        
        Returns
        -------
        TYPE: Transformed pandas DataFrame
        
        """
        X_merged = X.copy()
        X_merged = self._mergeLevels(X_merged)
        return X_merged



    def _mergeLevels(self,X):
        """
        Calls: None
        Called by: transform()

        Parameters
        ----------
        X : pandas DataFrame

        Returns
        -------
        X : pandas DataFrame: Transformed dataframe

        """
        for column, levels in self.featurewiseLevels_to_merge.items():
            X[column] = X[column].apply(lambda x: 'mothers' if x in levels else x)
        return X    


    def _learnLevelsBelowThreshold(self, X, **kwargs):
        """
        calls: None
        Called by: fit()
        
        What levels exist below the threshold?
        Parameters
        ----------
        X : pandas DataFrame
        kwargs : dictionary. Its keys are column names
                             and values are threshold.
                             Levels which occur below
                             the specified fraction
                             (threshold) are to be
                             merged.


        Returns
        -------
        None.

        """
        for column, threshold in kwargs.items():
            s = X[column].value_counts(normalize = True) <= threshold
            self.featurewiseLevels_to_merge[column] =  list(s[s == True].index)

            
    def levelsBeforeAfter(self, X, **kwargs):
        """
        What levels exist before and after the threshold per feature.
        Example:
            For a dataframe, df with two features featureName1 and featireName2, and
            respective merger thresholds as threshold1, threshold2, call as:
                
            levelsBeforeAfter(df,featureName1 = threshold1, featurename2 = threshold2)
            
            Or, as: 
                d = {'featureName1' : threshold1, 'featurename2' : threshold2}
                levelsBeforeAfter(df, **d)
                    
        Parameters
        ----------
        X : pandas DataFrame
        **kwargs : Keyword arguments
                   featureName1 = threshold1, featurename2 = threshold2

        Returns
        -------
        kwargs : dict of kwargs
        levelsbefore : dict of levelName:proportion-of-occurrences 
                       (above threshold)
        levelsafter :  dict of levelName:proportion-of-occurrences 
                      (below threshold)

        """
        
        
        
        self._learnLevelsBelowThreshold(X, **kwargs)
        levelsbefore = {}
        levelsafter = {}
        for column, levels in self.featurewiseLevels_to_merge.items():
            levelsbefore[column] = X[column].nunique()
            levelsafter[column] = X[column].nunique() - len(levels)
        return kwargs, levelsbefore,levelsafter    
        
        
 


"""   
# Uncomment and run this example
# Example:
    
# 1.0 Create a sample dataset
import pandas as pd
data = {
    'feature1': [5,4,2,2,1,3,0,0,1,0,0,0,3,5,0,1,4,4,5,4,3,1,1],
    'feature2': [0,0,1,3,1,1,3,0,3,0,3,1,4,1,4,3,5,1,0,5,5,1,2],
    'feature3': [5,2,1,4,1,4,2,0,1,4,1,2,2,5,5,4,1,5,3,5,5,3,1]
}

# 1.1
df = pd.DataFrame(data)
df    

# 1.2
s = df['feature1'].value_counts(normalize = True) <= 0.10
list(s[s == True].index)



# 1.3 Specifying thresholds for each feature as a dictionary
kwargs = {'feature1': 0.1, 'feature2': 0.2, 'feature3': 0.01}

# 2.0 Instantiate the class
merger_transformer = RareLevelMergerTransformer()
# 2.1
merger_transformer.fit(df, **kwargs)

# 2.2 
merger_transformer.levelsBeforeAfter(df, **kwargs)

# 2.3
merger_transformer.transform(df)

# 2.4
merger_transformer.featurewiseLevels_to_merge
X_merged = merger_transformer.transform(df)
X_merged
df

"""
    
#####################
    
