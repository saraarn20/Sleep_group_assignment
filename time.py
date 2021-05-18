def to_minutes(value):
  value = value / 10000000
  return ((value/60)/60)%24 * 60

print(to_minutes(36000000000))
print(to_minutes(3000000000))