# Data

In the previous part of the tutorial, you learned how to create a demographics questionnaire using several question polymorphs.

By the end of this part of the tutorial, you'll be able to store and download data.

Click here to see what your <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.2/blackboard.ipynb" target="_blank">`blackboard.ipynb`</a> and <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.2/survey.py" target="_blank">`survey.py`</a> files should look like at the end of this part of the tutorial.

## Previewing data from a single participant

Each hemlock project has a downloadable data frame containing the data for all participants. We'll start by looking at the data belonging to a 'test participant'.

Run the following in your jupyter notebook:

```python
from hemlock import Participant

part = Participant.gen_test_participant()
dict(part.get_data())
```

Out:

```
{'ID': [1],
 'EndTime': ['2021-02-10 15:34:28.116156'],
 'StartTime': ['2021-02-10 15:34:28.116156'],
 'Status': ['InProgress']}
```

This shows the data our test participant contributes to the data frame. The keys are variable names, and values are list of entries for that variable.

An easy way to add data is with 'embedded data':

```python
from hemlock import Embedded

part.embedded = [Embedded(var='MyVariable', data='MyData')]
dict(part.get_data())
```

Out:

```
{'ID': [1],
 'EndTime': ['2021-02-10 15:34:28.116156'],
 'StartTime': ['2021-02-10 15:34:28.116156'],
 'Status': ['InProgress'],
 'MyVariable': ['MyData']}
```

This adds an `Embedded` data object to our participant. Embedded data are a type of data element, like questions, but unlike questions, are not displayed to participants. We can add embedded data to a participant, branch, or page.

Looking at the data, we see that the participant has a new variable named `'MyVariable'` with data `['MyData']`.

## Ordering

Tl;dr When you have multiple data elements contributing data to the same variable, hemlock automatically orders them in a sensible way. If you find that your data frame isn't ordering your data the way you want, come back and reread this.

The order in which data elements appear in the data frame is the order in which they were added to the database; not necessarily the order in which they appear to the participant. For example:

```python
from hemlock import db

embedded1 = Embedded('MyVariable', 1)
embedded0 = Embedded('MyVariable', 0)
db.session.add_all([embedded1, embedded0])
db.session.flush([embedded1, embedded0])
part.embedded = [embedded0, embedded1]
dict(part.get_data())
```

Out:

```
{'ID': [1, 1],
 'EndTime': ['2021-02-10 15:34:28.116156', '2021-02-10 15:34:28.116156'],
 'StartTime': ['2021-02-10 15:34:28.116156', '2021-02-10 15:34:28.116156'],
 'Status': ['InProgress', 'InProgress'],
 'MyVariable': [1, 0]}
```

Note that the data for `'MyVariable'` are `[1, 0]` because we added `embedded1` before to the database before `embedded0` using `db.session.add_all` and `db.session.flush`.

Again, hemlock automatically manages your database, so you you'll only need to use `db.session.add_all` and `db.session.flush` in rare cases.

## Data rows

By default, data elements (embedded data and questions) contribute 1 row to the data frame. But we often want the same data to be repeated on multiple rows. We do this by setting the `data_rows` attribute:

```python
part.embedded = [Embedded('MyVariable', 'MyData', data_rows=3)]
dict(part.get_data())
```

Out:

```
{'ID': [1, 1, 1],
 'EndTime': ['2021-02-10 15:34:28.116156',
  '2021-02-10 15:34:28.116156',
  '2021-02-10 15:34:28.116156'],
 'StartTime': ['2021-02-10 15:34:28.116156',
  '2021-02-10 15:34:28.116156',
  '2021-02-10 15:34:28.116156'],
 'Status': ['InProgress', 'InProgress', 'InProgress'],
 'MyVariable': ['MyData', 'MyData', 'MyData']}
```

Additionally, we often want to 'fill in' rows of a variable to match the length of a data frame. For example, we may not know in advance how many rows a participant will contribute to the data frame, but we know that we want the participant's demographic information to appear on all rows. To do this, we set `data_rows` to a negative number. For example, `data_rows=-2` means 'fill in two rows with this data entry and, when you download the data, fill in any blank rows after this with the same data':

```python
part.embedded = [
    # these data will appear on three rows of the data frame
    Embedded('MyVariable', 'MyData', data_rows=3),
    # these data will fill in empty rows at the bottom of the data frame
    Embedded('MyFilledVariable', 'MyFilledData', data_rows=-1)
]
dict(part.get_data())
```

Out:

```
{'ID': [1, 1, 1],
 'EndTime': ['2021-02-10 15:59:28.018253',
  '2021-02-10 15:59:28.018253',
  '2021-02-10 15:59:28.018253'],
 'StartTime': ['2021-02-10 15:59:28.018253',
  '2021-02-10 15:59:28.018253',
  '2021-02-10 15:59:28.018253'],
 'Status': ['InProgress', 'InProgress', 'InProgress'],
 'MyVariable': ['MyData', 'MyData', 'MyData'],
 'MyFilledVariable': ['MyFilledData', 'MyFilledData', 'MyFilledData']}
```

Finally, a data element can contribute a list of values to the data frame:

```python
part.embedded = [Embedded('var', [0, 1, 2])]
dict(part.get_data())
```

Out:

```
{'ID': [1, 1, 1],
 'EndTime': ['2021-02-10 15:58:34.743335',
  '2021-02-10 15:58:34.743335',
  '2021-02-10 15:58:34.743335'],
 'StartTime': ['2021-02-10 15:58:34.743335',
  '2021-02-10 15:58:34.743335',
  '2021-02-10 15:58:34.743335'],
 'Status': ['InProgress', 'InProgress', 'InProgress'],
 'var': [0, 1, 2]}
```

## Adding data to our survey

We can add data to our existing survey in much the same way: by setting a question's `var` and (when necessary) `data_rows` attribute. We generally want demographics information to appear in all rows of the data frame, so we'll set `data_rows=-1`.

In `survey.py`:

```python
...

@route('/survey')
def start():
    return Branch(
        Page(
            Input(
                '<p>Enter your month and year of birth.</p>',
                type='month', var='DoB', data_rows=-1
            ),
            Select(
                '<p>What is your gender?</p>',
                ['Male', 'Female', 'Other'],
                var='Gender', data_rows=-1
            ),
            # SET THE `var` AND `data_rows` ATTRIBUTES FOR THE REST OF THE QUESTIONS
            ...
```

**Note.** When a participant submits a page, the questions' data are recorded in a `data` attribute. A question's data will be added to the data frame if and only if you set its `var` attribute. However, data will be stored in a question's `data` attribute whether or not the variable is set.

## Downloading data

Run your survey locally, fill in the demographics page, and continue to the end of the survey. Your data will be recorded in the database.

To download your data, navigate to <http://localhost:5000/download> in your browser. Select 'Data frame', then click the download button. This will download a zip file containing your data in `.csv` format.

Note that the data of questions for which you can select multiple choices are automatically one-hot encoded. For example, if `RaceWhite` and `RaceBlack` are both 1, and the rest of the race variables are 0, this means means the participant is part White and part Black.

## Summary

In this part of the tutorial, you learned how to store and download data.

In the next part of the tutorial, you'll implement validation for participant responses.