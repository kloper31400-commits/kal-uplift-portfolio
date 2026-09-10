# LinkedIn post: the speaker booking system

**Carousel, 5 real screenshots.** All captured from the live system, nothing staged.
Rebuild: `node scripts/capture-speaker-system.mjs 3000 kenneth-jones`
Files: `build/speaker-system/kenneth-jones/`

| # | File | What it shows |
|---|------|---------------|
| 1 | `01-application-redacted.png` | Kenneth's application as it lands in the dashboard: title, what he'd cover, three takeaways, why it matters now, bio, resources, ranked date choices, who it's for |
| 2 | `02-slot-board.png` | All 22 sessions, 11 booked, the rest open, with the tags saying whether the speaker was actually emailed and what they did with the invite |
| 3 | `03-onepager-redacted.png` | The one-pager generated from that application |
| 4 | `04-luma.png` | The public Luma event, carrying the same copy |

Alternate for #1: `build/speaker-system/jaron-rubenstein/01-application-redacted.png`.
Tighter card, and he applied yesterday, so it's the truest "I've never spoken to him" example.

Email addresses are blurred in the `-redacted` files. The unredacted originals sit beside them.

---

## The post

22 sessions in 8 weeks sounds great until you realize someone has to actually run 22 sessions in 8 weeks.

That's one of the problems I've been trying to solve with Uplift.

I want founders to have a menu of highly relevant, actionable sessions instead of putting everyone through the same handful of workshops.

But there's an obvious argument against that model:

It doesn't scale.

Every additional session traditionally means more sourcing, vetting, emails, scheduling, speaker prep, event copy, calendar invites, Luma setup, internal tracking, follow-ups.

Do that 22 times and you've basically created another job.

So instead of reducing the number of sessions, I've been trying to make the system for producing them repeatable.

Real screenshots below.

**1. This is Kenneth. He found Uplift and applied to speak.**

I'd never met him. But his application already tells me what he wants to teach, why founders need it now, the three things they'll walk away knowing, what he'll share, who it's for, and his ranked dates.

It arrives in my dashboard structured, sitting next to the sessions that still need a speaker.

**2. So my job is one question: is this worth our founders' time?**

If yes, I hit Approve. That claims the date, closes the slot, and refuses to let anyone else be booked into it.

You can see the whole board in the second screenshot. 11 booked, the rest open, and a tag on every booked session saying whether the speaker was actually emailed and what they did with the invite. That last part matters more than it sounds. A booked slot nobody told the speaker about is the failure that used to be invisible.

**3. Everything downstream is generated from that one application.**

His one-pager writes itself from his own answers. Title, session description, takeaways, who it's for, his bio, the resource he's sharing, the date, the format, what happens in his 30 minutes.

**4. And the public event page comes from the same source.**

Same words. Same takeaways. The application, the brief and the Luma page cannot drift apart, because they're all reading one record.

Then I send him the one-pager and a calendar hold, and ask him to grab 15 minutes with me the week before.

So I still spend 15 minutes with the human.

I just don't spend the hour of admin required to get us to those 15 minutes.

Do that 22 times.

That's 22+ hours of work I get back every single Uplift cycle. Almost three full workdays.

But that's not really the point.

The point is that 22 sessions become operationally possible.

And once the system exists, 30 sessions isn't an entirely new problem. Neither is another cohort. Or another program.

That's increasingly how I think about automation.

Not:

How can I automate my job?

But:

Which parts of my job actually require me?

My judgment requires me.
The 15-minute conversation requires me.
Understanding what our founders need requires me.

Writing the same event description for the 22nd time does not.

Next thing I want to build is the part that closes the loop.

Every session gets scored for usefulness. 7.5+ gets automatically invited back next cohort. But you have to earn that 7.5 every single time.

SOURCE → STRUCTURE → CURATE → EXECUTE → MEASURE → REPEAT

New expertise keeps entering.
Great sessions keep coming back.
Weak sessions fall out.
The curriculum stays current.

The goal isn't to run 22 sessions really well once. It's to build a system that can run 22 sessions really well again and again and again.

Don't make the programming smaller to make it scalable. Make the system underneath the programming scalable.
