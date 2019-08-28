select
PitcherId,
Pitcher,
round(((sum(sws) + sum(FB) + sum(InP) + SUM(HR)) * 1.0) / (sum(BALLS) + sum(cs) + sum(sws) + sum(FB) + sum(InP) + sum(HR)), 3) as swingPct,
round(((sum(FB) + sum(InP) + SUM(HR)) * 1.0) / ((sum(sws) + sum(FB) + sum(InP) + SUM(HR)) * 1.0), 3) as contactPct,
round(sum(sws) * 1.0 / (sum(BALLS) + sum(cs) + sum(sws) + sum(FB) + sum(InP) + sum(HR)), 3) as SwStrPct,
round(sum(sws) * 1.0 / ((sum(sws) + sum(FB) + sum(InP) + SUM(HR)) * 1.0), 3) as WhiffPct,
round(sum(fps) * 1.0/ COUNT(BatterId), 3) as FirstPitchStrikePct,
sum(FPCS) as FirstPitchCalledStrikes,
sum(FPSS) as FirstPitchSwingingStrikes,
round((sum(FPCS) * 1.0) / sum(Fps), 3) as PctOfCalledFirstPitchStrikes
from
logs_table
group by PitcherId