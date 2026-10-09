# Outreach CRM

A minimal, single-file CRM for Instagram DM outreach. Open `index.html` in a browser — no install, no server, no account.

## The loop

1. **Messages** – write 2–3 opener variants. Use `{first}`, `{name}`, `{handle}`, `{niche}` placeholders.
2. **Leads** – paste the IG accounts you've collected (one per line: `@handle`, `instagram.com/handle`, or `handle, Name, niche, followers`). Duplicates are skipped.
3. **▶ Start outreach** – walks through every new lead: shows the next variant (rotated evenly so each gets a fair test), copies it, opens the DM, and marks it sent.
4. **Update status** as replies come in: Replied → Interested → Call booked → Won (or Not interested / Ghosted). Use **+FU** to log follow-ups; leads with no reply after N days show as *follow-up due*.
5. **Dashboard** – response rate, positive rate, bookings, 14-day activity and a message leaderboard. Once a variant has enough sends (default 20), the best one is marked **WINNER**.
6. **Iterate** – archive the losers, click *Iterate* on the winner, change one thing, write down what you're testing. Repeat.

Winners are ranked by the lower bound of the 95% confidence interval on reply rate (Wilson score), so a lucky 2/3 doesn't beat a solid 12/60.

## Data

Everything is stored in your browser's localStorage. Use **Data → Export backup** regularly, and import it to move to another device or browser. Leads can also be exported to CSV.
