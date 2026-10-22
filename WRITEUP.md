# What my AI judge taught me about my own mistakes

I built an AI judge to grade the captions my AI writes for my sports Instagram account. On its first big disagreement with me, it was right and I was wrong: a stat I had marked as made up was sitting right there in the data. I was surprised, and glad it found the mistake. AI may not reason like a human, but it turned out to be very good at one job that matters: finding when something is not a proper match with the facts.

## The setup
@boxscorebrief is an Instagram page where I post the outcomes of my machine learning models that predict sports games, along with interesting stats I find using them. I have AI write the captions for two reasons: I wanted to see if an AI could read statistical data and turn it into a write-up the average person can understand, and I wanted the page to run as autonomously as possible.
That autonomy comes with a risk. If a caption has a wrong number, my audience could catch the mistake and stop trusting my data. Audience trust drives retention, and retention drives growth. And the page's whole pitch is honesty: I post every miss. I don't want to mislead anyone, so "is this caption accurate?" is the question everything else depends on.


## Building the measuring tape
I started with my real posts: 53 of them, each pairing the facts the AI was given with the caption it wrote. I split them by date. I built and tuned everything on the older posts and saved the newer ones for testing, so my scores show how the system does on posts it hasn't seen, like it would in real life.
Next I graded 30 posts by hand. For each one I marked whether it was factually correct, whether the automatic checker's warning (if any) was a real problem, and a quality score from 1 to 5. Those grades became my answer key.
Then I built two kinds of graders. Rule graders are plain code that check yes/no requirements: is every number in the facts, is the caption under 900 characters, does it end with a question, does it avoid betting language. They're fast, free, and consistent, but they can't understand meaning. For that I built an AI judge: Claude reads the facts and the caption and grades whether every claim is true, whether the post frames our pick as a loser, and its overall quality.
An AI judge is only useful if you can trust it, so I checked it against my answer key using Cohen's kappa, which measures how much the AI agrees with me beyond random chance.

## What the measurements found
The checker was wrong every time. My pipeline's automatic fact-checker had flagged 15 of the 30 posts I graded. When I checked them by hand, none of them contained a made-up number. I was surprised the checker was wrong every single time: it was tripping on hashtags like #49ers and on simple math like "a 57% favorite loses about 4 times in 10." Worse, I had rejected 3 accurate posts because of its warnings.
The AI judge and I caught each other's mistakes. The judge's first run agreed with my grades at a kappa of 0.44, only moderate. So I went through all 9 disagreements one by one. On the first one, the judge was right and I was wrong: a "35.7%" I'd marked as made up was in the data (as 0.357). It also caught real errors I had missed: a caption claiming Kansas City had "the biggest jump" when San Francisco's was bigger, one that described a model adjustment as an actual scoring margin, and one that invented a reason for the model's pick. Every number in those captions was correct, which is why no number-checker could catch them. But the judge was wrong sometimes too. It called reporting real losses "loser framing" until I made the rubric clearer. After fixing the mistakes on both sides, agreement rose to 0.61.
My own prompt was teaching the bad habit. Many captions described our picks as losers, like "an 85% favorite still loses 3 times in 20." I traced it back to my own instructions to the AI, which included the example "a 60% favorite loses 4 times in 10." The AI was copying it. I learned I have to be careful writing a prompt, because models treat examples as instructions.


## The fixes and the results
I made three changes to the writer's prompt, one for each problem I found: I replaced the example that taught "loser" framing, required "biggest" claims to be checked against every team, and explained that the model's factor amounts are adjustments to a prediction, not real stats.
On the 16 test posts, writing fresh captions with the same model and grading them blind, loser framing dropped from 9 to 0, judge-flagged factual errors from 2 to 0, and average quality rose from 3.38 to 4.81, for about 5% more tokens.
I also tested a Hermes agent that writes a draft, checks it with my rule graders, and revises. It tied the improved prompt on quality (4.81) and had zero real rule violations, but it used about 40 times as many tokens. For captions, the prompt fix was the better deal. My takeaway: start with the cheap one-shot prompt, and call the agent only when a cheap check fails.
One caveat: some of the errors that inspired the new prompt came from my test posts, so the test result may be slightly optimistic. To check, I set up a daily job that scores every new post with both prompts. On the first 6 brand-new posts, the new prompt matched or beat the old one on every post (4.50 → 4.83). That's too few to prove much yet, but the evidence grows every day.


## What I'd do differently, and what's next
If I started over, I would write stronger, more precise labels from the start. Two of my grades broke my own rule, and one "error" I marked wasn't an error at all. I'd also keep test posts completely out of sight while designing fixes. Some of the problems that inspired the new prompt came from my test set, which is why I added a daily check on brand-new posts.
The biggest weakness is sample size: 30 hand-labeled posts, 16 test posts, and 6 fresh ones. The results point in a consistent direction, but they're not proof yet.
I also learned that an agent's workspace is part of its input. Twice my Hermes agent saw files it shouldn't have (old captions, then leftover drafts), and both times it changed the results.
Next, I'll keep the daily job running so the fresh-post evidence grows, and I'll build adversarial test cases with planted fake stats to measure how often the checker and the judge actually catch invented numbers.
