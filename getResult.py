W = []

for i in range(50):
  line = raw_input().split()
  score = int(line[1])
  max_score = int(line[5])
  if max_score == 0:
    continue
  res = 1.0*score/max_score
  if score > 0:
    res += 0.2
  W.append(res)
print "Score:", 1.0*sum(W)/len(W)
