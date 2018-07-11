![InternetSpeedTester](internetspeedtester.png)
# Internet Speed Tester

## Introduction
The usefulness of testing one's bandwidth and latency speeds are virtually unquestionable. It is a way to hold an individual's internet service provider (ISP) responsible for guaranteed minimums and to provide more insight into why a network may be behaving the way it is. However, there are not many resources available to provide automated speed testing. Those that are in-browser require leaving the browser open to function, and may not provide latency values along with bandwidth data. The user is expected to trust the website without knowing what servers were used, in what location they were used, who owns the servers, and more.

Additionally, these websites may provide small amounts of flexibility in defining testing intervals. High fluctuations in connectivity may not be analyzed as easily if a user is given the choice of five minutes being the shortest amount of time between tests. Claims of these fluctuations may also be less credible to a particularly difficult or stubborn ISP in such a case.

### How does Internet Speed Tester differ from other testing programs?
This internet speed testing program seeks to redefine the niche of automated bandwidth/latency testing by providing improvements to the aforementioned flaws. Users of the program can define any number of minutes between testing intervals, so long as said number does not exceed the time between the start and end of the test. The program automatically generates a text file in its directory detailing the following:

* Download speed in Mbps
* Upload speed in Mbps
* Latency (ping) in ms
* A link to the user's test results
* The exact time at which the test was completed

These facets of Internet Speed Tester give the user a complete report of her network speed. She will easily be able to analyze what times her internet is at its worst, and what times it is at its best. The included links add a layer of trust to the results, granting her the ability to determine where each test was conducted.

## Dependencies
* Python 3 (developed on Python 3.6, to be exact)
* BeautifulSoup 4 and Selenium webdriver libraries
* Time and datetime libraries (built in)
* Tkinter GUI library (v. 8.6)
* requests library
* Chromedriver and geckodriver for automated Google Chrome / Firefox applications (included in repository)

Compiling an `exe` file is currently in the works for users that do not wish to take a developer's approach towards using the application. Otherwise, users are free to look at the pip-generated `requirements.txt` file listed within the repository for precise information about dependencies.

## Running the code
Internet Speed Tester can only be run within an integrated development environment (IDE) that supports the dependencies listed above. An executable file that is more user-friendly will be provided soon.

### Expected input and potential hiccups
IST has been developed with human error and mischief in mind. Bugs, however, are not uncommon in software, and I do not grant my application to be the exception. Feel free to report any issues or errors you run into - the more, the merrier, as there is no fixing software without valuable feedback.
#### Chrome and chromedriver
Running the program myself yielded issues with the Chrome option due to a bug that has not yet been fixed for the chromedriver application. The bug involves the `webdriver.click()` method functioning inconsistently, causing the program to hang and never close the webdriver. However, the most recent version (07/10/2018) of the application uses a workaround that _at least_ lessens the frequency of failure. I therefore advise users wanting to run the app seriously to choose Firefox as their browser of choice.
#### Expected input
IST expects the following input from users:

`Elapsed minutes per speedtest: ` _Any number between 1 and the number of minutes until the end of the speedtesting session_

`Time to end at: ` _Any number between 1 and 12_

`Choice of AM or PM (morning/evening) for session endtime`

Input errors are handled by displaying a popup informing the user of how he should format his input for the program to interpret.

## Potential future revisions
1. Graphical output of speed/latency versus the speedtest number.
2. Automated calculation of speed/latency averages.
3. Precise input for the program's "ending time."
4. Adding test cases to the repository.

## Fixes
_**07.10.2018:**_
> Implemented workaround for chromedriver bug, added requirements.txt to repository, wrote README content.
