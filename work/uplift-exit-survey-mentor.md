# Uplift Exit Survey — Mentors

**Goal order:** 1) confirm engagement and capture mentee outcomes from a second angle (funder data), 2) improve the mentor experience, 3) keep mentors engaged for future cohorts.
**Length target:** under 3 minutes, 14 questions.
**Linking:** personalized link with hidden fields (`email`, `first_name`, `mentee`). The mentee hidden field lets us pipe "your mentee, {{mentee}}" into question text and join mentor answers to the founder's record.

---

## Welcome screen

> Thank you for mentoring with Uplift. This takes about 2 minutes. Your answers close out your mentee's program record and shape how we run the next cohort.

---

## Section A — Your mentorship engagement

**1. What's your name?** *(short text, required)*
*Backstop in case a link goes out unpersonalized: the `first_name` hidden field should normally cover this silently, but this way no response comes back anonymous.*

**2. Did you and your mentee complete your mentorship engagement?** *(single select)*
*The application told mentors they'd be asked to confirm engagement at program end. This is that confirmation, and it feeds mentee completion sign-off.*
- Yes, we met as planned
- Partially, we met but less than planned
- No, we never connected

**3. Roughly how much time did you spend mentoring in total, across sessions and in-between support?** *(single select)*
- 1–2 hours
- 3–5 hours
- 6–10 hours
- More than 10 hours

**4. How would you rate the productivity of your one-on-one sessions with your mentee?** *(single select)*
- Very productive, we made real progress in nearly every session
- Productive, most sessions were useful
- Mixed, some sessions were more useful than others
- Not very productive, session time was often unfocused

**5. From your vantage point, how much progress did your mentee make during the program?** *(single select)*
- Significant progress
- Moderate progress
- A little progress
- No real progress
- Hard to say

**6. What did you see your mentee accomplish?** *(select all that apply)*
- Sharpened their priorities and next steps
- Improved their pitch or narrative
- Launched or shipped something
- Landed customers, users, or revenue
- Made progress on fundraising
- Made a major strategic decision (pivot, launch, expansion)
- Grew their confidence as a founder
- Other: ___
- Not sure / we didn't get that far

**7. How was the match between you and your mentee?** *(single select)*
- Excellent, exactly the kind of founder I can help
- Good
- Neutral
- Fair
- Poor fit

**8. Do you plan to keep in touch with your mentee now that the program is over?** *(single select)*
- Yes, we've already scheduled our next conversation
- Yes, informally as things come up
- Maybe
- No

---

## Section B — The program itself

**9. How likely are you to recommend mentoring with Uplift to a colleague?** *(0–10 opinion scale, NPS)*

**10. One thing the program did really well:** *(single select)*
- Mentor matching
- Onboarding and expectation-setting
- Program communication
- Session logging and the portal
- The midpoint meetup
- The Uplift Summit
- The time commitment
- Other: ___

**11. One thing we should improve for the next cohort:** *(single select, same list)*
- Mentor matching
- Onboarding and expectation-setting
- Program communication
- Session logging and the portal
- The midpoint meetup
- The Uplift Summit
- The time commitment
- Other: ___

**12. Anything that would make mentoring easier or more rewarding next time?** *(open text, optional)*

---

## Section C — Staying involved

**13. We'd like to continue to curate this community beyond the program sprint. Would you be interested in being part of an alumni group?** *(single select)*
- Yes, by email
- Yes, on WhatsApp
- Yes, either works
- No thanks

**14. To continue to find additional ways to engage, would you consider being a mentor in the next cohort?** *(single select)*
- Definitely, sign me up
- Probably
- Maybe, depends on timing and fit
- No

---

## Thank you screen

> Thank you for the hours you gave this cohort. We'll share the end-of-program impact report with you as soon as it's ready, so you can see what your mentorship added up to.

---

## Analysis notes (not in the survey)

- **Q1 (name) is a backstop, not the join key.** The `first_name` hidden field is what actually links a response to a mentee record; Q1 just keeps a response from coming back anonymous if a link goes out unpersonalized.
- **Q2 is operationally required:** mentee completion is contingent on mentor sign-off per the mentee application terms. Chase non-responders on this question alone if needed.
- **Q4 (productivity) is separate from Q5 (progress) on purpose:** a mentor can run focused, useful sessions even if the founder's outward progress was slow, and vice versa. Keeping them apart lets us tell "the mentoring was good but the founder wasn't ready" apart from "the sessions themselves weren't working," which points to different fixes (matching vs. mentor training/format).
- **Q5/Q6 give funders a second, independent read on founder outcomes**, useful to corroborate mentee self-reports.
- **Q13 (alumni group) leads Section C** because it's the lowest-commitment ask, then Q14 (mentor again) closes on the highest-commitment one, both framed around the same idea: continuing to engage with this community past the program sprint.
- Q10/Q11 use an identical list for a strengths vs. improvements chart, same pattern as the mentee survey.
