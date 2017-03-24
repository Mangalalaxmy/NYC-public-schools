One of the most controversial issues in the US educational system is the efficacy of standardized tests, and whether they are unfair to certain groups. Given our prior knowledge about this topic, investigating the correlations between SAT scores and demographic factors might be an interesting angle to take. We could correlate SAT scores with factors like race, gender, income, and more.

The SAT, or Scholastic Aptitude Test, is a test that high schoolers take in the US before applying to college. Colleges take the test scores into account when making admissions decisions, so it's fairly important to do well on. The test is divided into 3 sections, each of which is scored out of 800 points. The total score is out of 2400 (although this has changed back and forth a few times, the scores in this dataset are out of 2400). High schools are often ranked by their average SAT scores, and high SAT scores are considered a sign of how good a school district is.
Here are the links to all of the datasets we'll be using:

SAT scores by school -- SAT scores for each high school in New York City.
School attendance -- attendance information on every school in NYC.
Class size -- class size information for each school in NYC.
AP test results -- Advanced Placement exam results for each high school. High schools students in the US can choose to take AP exams. There are several AP exams, one for each subject. Passing an AP exam can get you college credit in that subject.
Graduation outcomes -- percentage of students who graduated, and other outcome information.
Demographics -- demographic information for each school.
School survey -- surveys of parents, teachers, and students at each school.
All of these datasets are interrelated, and we'll need to combine them into a single dataset before we can do the correlations we want.
From looking at these, we can learn a few things:

The SAT is only administered to high schoolers, so we'll want to focus on high schools.
New York City is divided into 5 boroughs, which are essentially distinct regions.
Schools in New York City are divided into several school districts, each of which can contains dozens of schools.
Not all the schools in all of the datasets are high schools, so we'll need to do some data cleaning.
Each school in New York City has a unique code called a DBN, or District Borough Number.
By aggregating data by district, we can use the district mapping data to plot district-by-district differences.
 Here are all the files in the schools folder:

ap_2010.csv -- contains data on AP test results.
class_size.csv -- contains data on class size.
demographics.csv -- contains data on demographics.
graduation.csv -- contains data on graduation outcomes.
hs_directory.csv -- a directory of high schools.
sat_results.csv -- data on sat scores.
survey_all.txt -- data on surveys from all schools.
survey_d75.txt -- data on surveys from New York City district 75.
survey_all.txt and survey_d75.txt are in more complicated formats than the rest of the files. For now, we'll focus on reading in the csv files only, and then explore them.
The Dataframe combined contains all of our data, and is what we'll be using in our analysis.
