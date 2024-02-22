from fast_string_match import closest_match as clm, closest_match_distance as closest_match

names = ['cop','sip','sop','soprano','soprano-blue','soprano-green','dephnnie', '༒']
m = closest_match('dephn',names)
print(m)
n = clm('dephn', names)
print(n)