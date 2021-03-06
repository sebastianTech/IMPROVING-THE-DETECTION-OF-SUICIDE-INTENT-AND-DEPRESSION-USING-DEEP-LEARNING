# -*- coding: utf-8 -*-
"""Suicide detection [ Bi-variate,Uni-variate] Data preprocessing

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1r94HQbYWMW6npwJghYHeD9nL11QnTW4w
"""

from google.colab import drive
drive.mount('/content/drive')

pip install chart-studio



# Commented out IPython magic to ensure Python compatibility.
## Importing Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly as plty
from chart_studio import plotly
import plotly.graph_objs as go
import plotly.figure_factory as ff
import plotly.tools as tls
import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)
import scipy.stats #for a bit of statistiscs
# %matplotlib inline

test = pd.read_csv("/content/drive/MyDrive/UoB Dissertation Folder/foreveralone...csv")

test.head()

test.shape

test['attempt_suicide'].value_counts(normalize=True)

test['depressed'].value_counts(normalize=True)

test['social_fear'].value_counts(normalize=True)

test['race'].value_counts(normalize=True)

test['edu_level'].value_counts(normalize=True)

# change dataype to int
test['friends'] = test['friends'].astype(np.int64)

#drop rows with null values
test.dropna(inplace=True)

# strip stings with white space
test['job_title'] = test.job_title.str.strip()

# Function to replace job_title values
def replace_text(what, to):
    test.replace(what, to, inplace= True)

replace_text('student', 'Student')
replace_text('none', 'None')
replace_text("N/a", 'None')
replace_text('na', 'None')
replace_text('-', 'None')
replace_text('.', 'None')
replace_text('*', 'None')
replace_text('ggg', 'None')

test.job_title.value_counts()

# body weight
test.bodyweight.value_counts()

# sexuality freqency

test.sexuallity.value_counts()

"""# Univariate Analysis

"""

test.gender.value_counts()

"""Univariante Analysis

Variables visualisation based on data type: Categorical, ordinal and numerical.

Categorical features:(Gender, depressed, attempt_sucide,sexuality)

Ordinal features:(age, Education,)

Numerical features:(Income)
"""

test['gender'].value_counts(normalize=True).plot.bar(title='gender')
plt.show()
test['depressed'].value_counts(normalize=True).plot.bar(title='depressed')
plt.show()
test['attempt_suicide'].value_counts(normalize=True).plot.bar(title='attempt_suicide')
plt.show()
test['sexuallity'].value_counts(normalize=True).plot.bar(title='sexuallity')
plt.show()
test['bodyweight'].value_counts(normalize=True).plot.bar(title='bodyweight')
plt.show()

"""Independent Variable (Ordinal)"""

test['age'].value_counts(normalize=True).plot.bar(figsize=(12,2), title='age')
plt.show()
test['edu_level'].value_counts(normalize=True).plot.bar(figsize=(12,2), title='edu_level')
plt.show()

Gender=pd.crosstab(test['gender'],test['attempt_suicide'])
Gender.div(Gender.sum(1).astype(float), axis=0).plot(kind="bar",stacked=True,figsize=(4,4))
plt.show()

Age=pd.crosstab(test['age'],test['attempt_suicide'])
Depressed=pd.crosstab(test['depressed'],test['attempt_suicide'])
Sexuality=pd.crosstab(test['sexuallity'], test['attempt_suicide'])
Body_weight=pd.crosstab(test['bodyweight'],test['attempt_suicide'])
Age.div(Age.sum(1).astype(float), axis=0).plot(kind="bar",stacked=True,figsize=(20,4))
plt.show()
Depressed.div(Depressed.sum(1).astype(float), axis=0).plot(kind="bar",stacked=True,figsize=(4,4))
plt.show()
Sexuality.div(Sexuality.sum(1).astype(float), axis=0).plot(kind="bar",stacked=True,figsize=(4,4))
plt.show()
Body_weight.div(Body_weight.sum(1).astype(float), axis=0).plot(kind="bar",stacked=True,figsize=(4,4))
plt.show()

matrix = test.corr()
f, ax = plt.subplots(figsize=(9,6))
sns.heatmap(matrix,vmax=.8,square=True,cmap="BuPu", annot = True)

test.describe()

fig, ax = plt.subplots()
# ax.set_ylim(0, 105)
# whiskers on 0.3 and 99.7 percentile to determine outliers
test.boxplot(column='friends', ax=ax, whis=[0.3,99.7])

test.loc[test['friends'] <= 50,:] \
        .groupby('attempt_suicide')['friends'] \
        .plot.hist(legend=True, density=True, alpha = 0.5)

test['improve_yourself_how'].head(15)

test['improve_yourself_how'] = test['improve_yourself_how'].str.lower()
# none isn't an improvment, so we don't need to count it
test['total_improves'] = test['improve_yourself_how'].str.split(',').apply(lambda x: len([i for i in x if i != 'none']))
test.groupby('attempt_suicide')['total_improves'].plot.hist(legend=True, density=True, alpha = 0.5)

improvements = test['improve_yourself_how'].str.split(',').apply(pd.Series).stack().reset_index(drop=True)
improvements = improvements.str.strip()
top_improvements = improvements.value_counts()

top_improvements.plot(kind='bar')

# Most of improvements found in the dataset only once. 
# Actually there are some mistypes and values with pretty similar sense. But for now let's leave it as it is.
# As far as they can't help us to understand polulation, it's good idea to remove these improvements

top_improvements = top_improvements[top_improvements > 5]

top_improvements.plot(kind='bar')

# Much better.
# Now lets add these improvements to the data set as new features

for imp in top_improvements.index:
    test['[improve] {}'.format(imp)] = test['improve_yourself_how'].str.contains(imp, regex=False)

col = {x:'sum' for x in test.columns if '[improve]' in x}
test.groupby('attempt_suicide').agg(col).apply(lambda x: x/x.sum(), axis=1)

test['income'] = test['income'].apply(lambda x: x.split("$")[-1])

test['income'].value_counts()

plt.figure(figsize=(15,5))
sns.countplot('age',data=test)

plt.figure(figsize=(15,5))
sns.countplot('income',data=test)

"""What is the most common way in which people try to improve themselves?
What is the most common favour that people want?
Is there a relationship between depression and virginity?
Is there a relationship between bodyweight and virginity?

The first two questions are simple aggregations. They don't need a lot of thinking about. The nex three however, need a little more code and they do produce some rather unexpected results. So, let's start!
"""

test["what_help_from_others"].unique()

"""So, let's get on with the analysis. First up, which is the most common method of help that people want from others? To answer this, we'll need to look at the what_help_from_others column.

A few things pop out on looking at the result above:

There seem to be more than one answer per responder
The answers are all separated by a comma.
There are a few custom answers. I guess that these people had a lot of time on their hands (self-evident. They're single XD ).
So here's what we'll do:

We'll split based on the comma
We'll get the counts of each of the entries. Also, there's this entry "I don't want help". We'll ignore that.
We can do this programatically. But, there's another (pandas) method to help us do this: .get_dummies()
"""

# getting the most common form of help people want
test[test["what_help_from_others"] != "I don't want help"]["what_help_from_others"].str. \
    get_dummies(",").sum().sort_values(ascending = False)[:10]



"""Joining a gym seems to be the most common option to improve oneself. Honestly, I don't understand these people? Why join a gym when you can craft the bod-of-your-dreams at your local park with calisthenics? I bet that it's a sure fire way to get more people to notice you.

The third question: What's the relationship between depression and virginity? This is a pretty cool question. Seeing how reports of depression are reaching sky-high levels, this might shed some light into the problem.
"""

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
sns.set()
plt.style.use("ggplot") # yea, I still love ggplot2

sns.countplot(x = "virgin", data = test, hue = "depressed")



"""There seem to be more depressed people among virgins. There seem to be more depressed people among non-virgins. Overall, there seem to be more depressed people.

But, if we look at the percent differences in each of the categories, clearly, the difference is higher amongst the people who are virgins. This difference is 25% in the non-virgin group and a staggering 135% in the virgin group.

But, is this the true relationship? Is there a deviation from the expected value and is this deviation significant? Let's check it out.
"""

scipy.stats.chisquare(f_obs = [52, 65, 105, 247], f_exp = [39, 78, 118, 234]) 
# expected values were calculated by hand

"""Well, the observed relationship does seem to differ from what it's supposed to be. Now, if assume that their depression is not caused by any other factor (we might ignore these since trying to measure them is too much work), we can ask a follow up question: Are the virgins single because they are depressed? Or are they depressed because they are single?

Even though we ignored other causes of depression, it's more likely that the people who are depressed have a hard time finding a partner because of their depression, which makes it hard for them to communicate. Cool.

The last question: Is there a relationship between bodyweight and virginity? This is a pretty interesting one. We saw earlier that the most common choice for self-improvement was to join a gym. Assumably, this has something to do with weight and/or appearance. People who are over weight are looking to lose the love handles, while those who are underweight are probably looking to get healthy. While those who are in the normal range might want to shape their bodies properly to attract more potential partners.

Enough talk. Let's get to the code.
"""

sns.countplot(x = "virgin", data = test, hue = "bodyweight")
plt.title("Bodyweight and virginity")
plt.xlabel("Are you a virgin?")

test.pivot_table("age", index = "virgin", columns = "bodyweight", aggfunc = "count")

"""As with the previous categorical relationship, we'll check if the observed relationship is different from the actual. [I've calculated the expected values by hand. The formula for calculating expected values is E(i, j) = (T(i) * T(j)) / N where E(i, j) is the expected value in the ith row and jth column T(i) is the total for the ith row T(j) is the total for the jth column and N is the overall total. ]"""

# chisquare test on virginity and bodyweight
scipy.stats.chisquare(f_obs = [77, 7, 25, 8, 192, 18, 88, 54], 
	f_exp = [67.10, 6.23, 28.19, 15.46, 201.89, 18.76, 84.81, 46.53])



"""Whuuut?! The relationship between virginity and bodyweight doesn't seem to deviate too much from the actual relationship. If so, then why do so many people join the gym as a means to improve themselves? It's pretty counter intuitive.
Man alive, this is a cool finding.
"""