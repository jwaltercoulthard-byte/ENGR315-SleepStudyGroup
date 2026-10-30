# Sleep Quality Quantification Program

**Team:** The Sleep Supporters (Group 1)

**Authors:** Declan Pitsinger, Joseph Herberger, James Coulthard

## Table of Contents

- [Objective and Motivation](#objective-and-motivation)
- [Dataset](#dataset)
- [Project Questions](#project-questions)
- [Implementation Details](#implementation-details)
- [Results](#results)
- [Conclusions](#conclusions)
- [Actions To Complete](#actions-to-complete)
- [References](#references)

---

## Objective and Motivation

The goal of this project is to create a system that can determine the quality of an individual's sleep for a single 24-hour period.

Data was collected from each participant using two devices worn 24 hours a day:

- **Heart rate monitor:** Polar H7
- **Actigraph:** ActiGraph wGT3X-BT

Twice a day, before going to bed and before waking, participants collected home saliva samples in vials. These were used to extract RNA and to measure clock genes, melatonin, and cortisol.

The data was collected to provide a high-level dataset from wearable activity trackers, which have become more popular in recent years. Ideally, it can be used to predict a person's well-being and to develop better tools for analyzing a person's current health state.

> "This data set enables researchers to test the correlations between physical activity and sleep quality."

## Dataset

**Source:** [Multilevel Monitoring of Activity and Sleep in Healthy People](https://doi.org/10.13026/cerq-fc86) (PhysioNet)

Key data categories used in this project:

| Category | Description |
| --- | --- |
| Total sleep time | Total time spent asleep |
| Number of awakenings | Awakenings during the night |
| Average awakening length | Mean duration of awakenings |
| `ibi_s` | Heart beat intervals |
| PSQI | Pittsburgh Sleep Quality Questionnaire |
| Daily stress | Self-reported daily stress |

These and other fields can serve as a baseline for a person's sleep quality, especially by using good nights of sleep as the reference to compare against.

## Project Questions

### Q1: Average heart rate and number of spikes over time

Heart rate patterns over a night are a direct window into sleep stress and restlessness. This becomes inferential when asking whether the spike count differs significantly between sleep stages or between nights, comparing spike count against time of night or night-to-night condition.

### Q2: Accelerometer data for restless sleeping

Movement is a simple, non-invasive proxy for sleep disruption. It is inferential when testing whether movement levels differ between good and poor sleepers (or high and low heart-rate nights), comparing accelerometer magnitude against sleep quality group.

### Q3: Swab levels (cortisol, melatonin) vs. acceptable levels

Hormone levels give a biochemical check on what the wearable signals suggest about stress and circadian rhythm. It is inferential because we test whether a person's or sample's mean hormone level differs from a reference range, comparing measured cortisol/melatonin against clinical reference values.

### Q4: Defining individual inputs to select baseline metrics

Personalizing baselines (age, sex, weight, etc.) keeps the program from flagging normal variation as abnormal. It is inferential if we test whether baseline metrics differ across demographic groups, comparing resting heart rate or hormone levels against individual input variables.

### Q5: Sleep quality index vs. acceptable ranges

A single summary score is the most practical output for an end user. It is inferential when testing whether the index differs significantly from the acceptable range, or from group to group, comparing sleep quality index against threshold range or user group.

### Summary

| Question | What we will make | Dataset elements | How they're used |
| --- | --- | --- | --- |
| **Q1** | A graph of heart rate (bpm) over time of night with the number of spikes marked and counted. | Heart rate column, timestamp column | Compute the mean heart rate per night and count readings above a spike threshold, then compare across time windows or nights. |
| **Q2** | A graph of acceleration magnitude (g) over time of night, with areas of restless sleep indicated. | Accelerometer x/y/z columns (or the magnitude vector), timestamp, sleep stage/quality label | Combine x/y/z into one movement magnitude, then compare between sleep quality groups or stages. |
| **Q3** | A table of before, after, and baseline hormone values, with the comparison and the error above or below baseline. | Cortisol and melatonin columns, sample time, reference range values | Compare measured hormone levels to external reference ranges (a one-sample comparison). |
| **Q4** | Feeds the final summary table (combined with Q5): baseline values chosen from the individual's inputs. | Demographic/user-input columns (age, sex, weight, etc.), resting heart rate, hormone baselines | Group baseline metrics by user characteristics to see which inputs meaningfully shift the baseline. |
| **Q5** | A final summary table (combined with Q4) with baseline/acceptable values, this study's values, the sleep quality index, and a good/bad sleep night rating. | Sleep quality index (or a composite of heart rate, movement, and hormone columns), reference range | Compare the index to the acceptable range, or between groups, to flag poor sleep. |

## Implementation Details

### Question 1: Heart Rate Monitoring
**Methods/Metrics:** This data is presented in a csv file which would need to be read and put into an array of values which can be iterated over to find a time heart rate pairing which can be put into a plot to show how the heart rate changes and to visualize such data.  This would be a more human centered approach comparing the heart rates of two sleepers one good and one bad and visually comparing such data.  On a metrical view the average heart rate can be calculated for the nights sleep and using python the heart rates can be iterated through to find areas with spikes or times when the heart rate is above a normal threshold how long you were in that threshold and how high your heart rate went.  These can be compared numerically against each other in sleepers.  

**Resources:** Ideally, no extra python packages will be needed beyond what has been used so far.  

**Plots:** The plots created would be a normal XY graph showing a heart rate over a time period.


### Question 2: Sleep Restlessness
**Methods/Metrics:** The Accelerometer data comes in a csv thus it can be easily iterated through with each time stamp to find a magnitude for that time moment which can be used for comparison.  The X/Y/Z data could again be placed into 3 separate arrays and iterated through each at one with an equation to create the magnitude and stored into a separate array.  This will be used to find a max magnitude in the night, average magnitude across the night, and how many active spikes there were in the data.  Each could be graphed against a time creating an XY graph with time on the X axis and the magnitude on the Y showing spikes and visualizing the data.

**Resources:** Ideally, No extra packages would be needed beyond what has already been used.

**Plots** The plots above would be enough to visualize the data and make significant inferences from it.


### Question 3: Hormone level changes
**Methods/Metrics:** The data is a specific point for morning and night and only taken twice a day so values per day can be compared against an external source for normal morning and night values.  These values would not be too beneficial on their own but would serve as a benchmark across multiple days or as an outlier in data.  Each night in a week can be compared on a bar graph against a preset average or ideal value showing a direct comparison, showing the magnitude of such two differences.  

**Resources:** The plots would not require any extra packages and could be down just using Python.  

**Plots:** The bar graph would be the most ideal for comparing against a set value for each individual day. 


### Question 4/5: Metrics and SQI 
**Methods/Metrics:** This question involves more data than an individual column and acts as a comparison question between good and bad sleep with each individual's values and baselines being determined based on set criteria.  The baseline values in question 4 are what each individual participant would collect and enter including age, sex, weight, etc which would create a baseline metric to compare each individual on in a fair way as each individual is unique.  Creating these equations can be with equations or based on a lookup chart previously created from a study or research paper.  Taking these created baseline values they can be compared to acceptable baseline values proven for good sleep for each criteria and can be displayed in a table or chart along with error or percentage differences away from the baseline displayed for each category indicating where this individual is suffering with bad sleep. 

**Resources:** This data might require extra packages but should be able to be completed using numPy and previously used packages. 

**Plots:** The data can be formatted in a table as a graph or plot would not be effective to visualize this data as it is raw numbers rather than a change over time.  The sleep quality index and individual values could be compared across a daily log of time for a week or a month to create a trend graph showing an increase or decrease or consistent elevation or decline in sleep quality index over a period of time and can be used in conjunction with other graphs to provide a visualization of the data.


## Results

*(Answers to the questions; sub-task 6)*

_TODO_

## Conclusions

*(Sub-task 7)*

_TODO_

## Actions To Complete

- [ ] _TODO_

## References

Rossi, Alessio, et al. "Multilevel Monitoring of Activity and Sleep in Healthy People" (version 1.0.0). *PhysioNet* (2020). RRID:SCR_007345. https://doi.org/10.13026/cerq-fc86
