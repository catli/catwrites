Title: A/A Before A/B 
Slug: aa_before_ab_testing
Date: 2015-02-01


## WHY YOU SHOULD ALWAYS START A/B TESTING WITH A/A TESTING

Earlier, we talked about how an A/B testing framework can be used to better understand and improve technology-based learning for students. A/B testing creates two slightly different designs (for example one with a green background and one with a pink background) and randomly assign students to each group. How do we know then whether students like the pink or the green background better? We randomly assign students to each group and then compare how studentsin each group rate their activities. Then we can just start comparing the results until we see significant differences - right? Hmm…not quite…, at least according to this [one paper](http://www.qubit.com/sites/default/files/pdf/most_winning_ab_test_results_are_illusory.pdf), most statistically significant A/B test results are illusory.

And this has a lot to do with the [statistical power](https://en.wikipedia.org/wiki/Statistical_power) of the test, that is the likelihood of a false positive in the test. When we evaluate the results of the two groups, we often focus on the p-value of the delta. Since the sample size in this case is not fixed and we can choose when we declare a winning design, we end up evaluating the results at different intervals over the course of the experiment, and creating a multiple comparisons problem, which cannot be evaluated with the normal t-test for significance.

One way to avoid this is to use a A/A test (null test), described on page 79 of [Web Analytics Demystified](http://www.webanalyticsdemystified.com/downloads/Web_Analytics_Demystified_by_Eric_Peterson.pdf). We can run the A/A test results by setting up an experiment where the design for both groups is exactly the same or we can simulate an A/A test by randomly sampling from existing historical data. The advantage of the A/A test is that we know that the true delta for the data is 0. If we look at many different iterations of the same sample sizes, we start to see the distribution of a false positive at different sample sizes given the true value is 0. We can use results from the null test to figure out the minimum sample size we need before we can start peeking at our test results. 

    :::R
    sample(...,replace=TRUE)

