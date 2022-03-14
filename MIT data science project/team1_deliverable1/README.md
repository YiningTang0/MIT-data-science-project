# Brief Update

**Data Source**

We scrape the website http://collaboration.mit.edu/ to get a .csv data file, which contains the name of each professor, along with the rank, department, article count, conference proceeding count, grant count, patent count, and course count.

**Scope Refinement**

Since the main focus on this project is the difference in number of applications, patents, papers, and/or conference proceedings by gender and by race, we found that ther are departments (e.g. Anthropology) do not necessiraly have patent applications. Thus, we reduce the data scope to the professors from a list of departments:
- Aeronautics and Astronautics
- Biological Engineering
- Biology
- Brain and Cognitive Sciences
- Chemical Engineering
- Chemistry
- Civil and Environmental Engineering 
- Electrical Engineering and Computer Sciences
- Materials Science and Engineering
- Mechanical Engineering
- Media Arts and Sciences
- Nuclear Engineering
- Physics

**Gender Classification**

Since the dataset we scraped from the website does not include gender and race information, we want to first deal with the gender matter. We found a dataset of names and their corresponding gender online, trained this dataset and built a model to classify the gender of faculties.

- Link of training dataset: https://archive.ics.uci.edu/ml/datasets/Gender+by+Name
- Gender classification model: see gender_classification.ipynb

**Question to be Answered**

In this deliverable, we are going to answer the first analysis question:

Is there a statistically significant disparity by race and/or gender in patent applications, patents, papers, and/or conference proceedings relative to the representation in each department or overall at MIT?